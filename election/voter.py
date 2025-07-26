import streamlit as st, mysql.connector, time, io
from PIL import Image

class Voting:
    def __init__(self):
        header_placeholder = st.empty()

        conn = mysql.connector.connect(host='localhost', user='root', password='12345678')
        cursor = conn.cursor()
        cursor.execute("USE Student_Election;")

        cursor.execute("SELECT status FROM users WHERE user_id = %s", (st.session_state.user_id,))
        status = cursor.fetchone()[0]

        if status != 1:
            st.empty()
            header_placeholder.empty()
            with header_placeholder.container():
                st.header("❌ Voting Is Not Currently Available for this Device")
            time.sleep(2)
            st.rerun()
            return

        header_placeholder.empty()
        with header_placeholder.container():
            st.header("✅ Voting Has Been Allowed for this Device")
            time.sleep(0.5)
        header_placeholder.empty()
        
        cursor.execute("SELECT DISTINCT Standing_For FROM candidates")
        positions = cursor.fetchall()

        form_placeholder = st.empty()
        success_placeholder = st.empty()
        error_placeholder = st.empty()

        form_key = f"form_{st.session_state.user_id}"

        with form_placeholder.form(form_key, True):
            selections = []

            for pos in positions:
                position = pos[0]
                st.subheader(f"Position: {position}")

                cursor.execute("SELECT Name, picture FROM candidates WHERE Standing_For = %s", (position,))
                candidates_data = cursor.fetchall()

                candidates = []
                images_bytes = []

                for candidate_row in candidates_data:
                    candidates.append(candidate_row[0])
                    images_bytes.append(candidate_row[1])

                cols = st.columns(len(candidates))
                for i in range(len(candidates)):
                    image = Image.open(io.BytesIO(images_bytes[i]))
                    with cols[i]:
                        st.image(image, use_container_width=True)
                        st.caption(candidates[i])

                radio_key = f"{st.session_state.user_id}_{position}"
                
                if radio_key not in st.session_state:
                    st.session_state[radio_key] = None

                selected_candidate = st.radio(
                    f"Select your candidate for {position}",
                    candidates,
                    index=None,
                    key=radio_key
                )
                selections.append(selected_candidate)

            submitted = st.form_submit_button("Submit")

        if submitted:
            if None not in selections:
                for pos_index in range(len(positions)):
                    position = positions[pos_index][0]
                    selected_name = selections[pos_index]

                    cursor.execute(
                        "UPDATE candidates SET votes = votes + 1 WHERE Name = %s AND Standing_For = %s",
                        (selected_name, position)
                    )
                conn.commit()

                form_placeholder.empty()
                with success_placeholder.container():
                    st.success("✅ Your votes have been recorded. Thank you!")
                time.sleep(1)
                success_placeholder.empty()

                cursor.execute("SELECT voter_Adno FROM users WHERE user_id = %s", (st.session_state.user_id,))
                Adno = cursor.fetchone()[0]
                cursor.execute("UPDATE voters SET voting_status=1 WHERE barcode = %s", (Adno,))
                cursor.execute("UPDATE users SET status=0 WHERE user_id = %s", (st.session_state.user_id,))
                conn.commit()
                st.rerun()
            else:
                with error_placeholder.container():
                    st.error("⚠️ Please vote for all positions before submitting.")
