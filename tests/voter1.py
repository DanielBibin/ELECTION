import streamlit as st, mysql.connector, time, io
from PIL import Image

class Voting:
    def __init__(self):
        header_placeholder = st.empty()

        # Connect to DB
        conn = mysql.connector.connect(host='localhost', user='root', password='12345678')
        cursor = conn.cursor()
        cursor.execute("USE Student_Election;")

        # Check status
        while True:
            cursor.execute("SELECT status FROM users WHERE user_id = %s", (st.session_state.user_id,))
            status = cursor.fetchone()[0]
            if status == 1:
                break
            header_placeholder.empty()
            with header_placeholder.container():
                st.header("❌ Voting Is Not Currently Available for this Device")
            time.sleep(2)
            st.rerun()

        # Voting allowed
        header_placeholder.empty()
        with header_placeholder.container():
            st.header("✅ Voting Has Been Allowed for this Device")
            time.sleep(0.5)
        header_placeholder.empty()

        # Get positions
        cursor.execute("SELECT DISTINCT Standing_For FROM candidates")
        positions = cursor.fetchall()

        form_placeholder = st.empty()
        success_placeholder = st.empty()

        # ✅ Clear session state BEFORE form to avoid previous votes showing up
        if "cleared" not in st.session_state or not st.session_state.cleared:
            for key in list(st.session_state.keys()):
                if key.startswith("radio_") or key.startswith("Voting_Form_"):
                    del st.session_state[key]
            st.session_state.cleared = True

        # Stable form key
        form_key = f"Voting_Form_{st.session_state.user_id}"
        with form_placeholder.form(form_key):
            selections = []

            for pos in positions:
                position = pos[0]
                st.subheader("Position: " + position)

                # Fetch candidates
                cursor.execute("SELECT Name, picture FROM candidates WHERE Standing_For = %s", (position,))
                candidates_data = cursor.fetchall()

                candidates, images_bytes = [], []
                for c in candidates_data:
                    candidates.append(c[0])
                    images_bytes.append(c[1])

                cols = st.columns(len(candidates))
                for i in range(len(candidates)):
                    image = Image.open(io.BytesIO(images_bytes[i]))
                    with cols[i]:
                        st.image(image, use_container_width=True)
                        st.caption(candidates[i])
                while len(selections) != len(candidates):
                    if st.session_state.user_id not in st.session_state.keys():
                        selected_name = st.radio("Select your candidate for " + position, candidates, index=None, key = st.session_state.user_id)
                
                    selections.append(selected_name)
                    submit_button = st.form_submit_button("Submit")

        if submit_button:
            st.write("DEBUG: Selections ->", selections)
            if all(selections):
                for pos, selected_candidate in zip([p[0] for p in positions], selections):
                    cursor.execute(
                        "UPDATE candidates SET votes = votes + 1 WHERE Name = %s AND Standing_For = %s",
                        (selected_candidate, pos)
                    )
                conn.commit()

                form_placeholder.empty()
                with success_placeholder.container():
                    st.success("✅ Your votes have been recorded. Thank you!")
                time.sleep(1)
                success_placeholder.empty()

                # Mark user as voted
                cursor.execute("SELECT voter_Adno FROM users WHERE user_id = %s", (st.session_state.user_id,))
                Adno = cursor.fetchone()[0]
                cursor.execute("UPDATE voters SET voting_status=1 WHERE barcode = %s", (Adno,))
                cursor.execute("UPDATE users SET status=0 WHERE user_id = %s", (st.session_state.user_id,))
                conn.commit()

                # Clean up
                for key in list(st.session_state.keys()):
                    if key.startswith("radio_") or key.startswith("Voting_Form_"):
                        del st.session_state[key]
                st.session_state.cleared = False
                st.rerun()
            else:
                st.error("⚠️ Please vote for all positions before submitting.")
