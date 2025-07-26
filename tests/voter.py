import streamlit as st, mysql.connector, time, io
from PIL import Image

class Voting:
    def __init__(self):
        header_placeholder = st.empty()
        conn = mysql.connector.connect(host = 'localhost', user = 'root', password = '12345678')
        cursor = conn.cursor()
        cursor.execute("USE Student_Election;")
        cursor.execute("SELECT status FROM users WHERE user_id = %s", (st.session_state.user_id, ))
        status = cursor.fetchone()[0]
        while status == 0:
            header_placeholder.empty()
            with header_placeholder.container():
                st.header("❌ Voting Is Not Currently Available for this Device")
            cursor.execute("SELECT status FROM users WHERE user_id = %s", (st.session_state.user_id, ))
            status = cursor.fetchone()[0]
           
        
        header_placeholder.empty()
        with header_placeholder.container():
            st.header("✅ Voting Has Been Allowed for this Device")
            time.sleep(.5)
        header_placeholder.empty()
        cursor.execute("SELECT DISTINCT Standing_For FROM candidates")
        positions = cursor.fetchall()
        form_placeholder = st.empty()
        with form_placeholder.form("Voting_Form"):
            selections = []

            for pos in positions:
                position = pos[0]
                st.subheader("Position: "+position)
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

                selected_name = st.radio("Select your candidate for "+position, candidates, index=None, key=position)
                selections.append(selected_name)

            submit_button = st.form_submit_button("Submit")

        if submit_button:
            if selections:
                for selected_candidate in selections:
                    cursor.execute(
                        "UPDATE candidates SET votes = votes + 1 WHERE Name = %s AND Standing_For = %s",
                        (selected_candidate, position[candidates.index(selected_candidate)])
                    )
                conn.commit()
                form_placeholder.empty()
                st.success("✅ Your votes have been recorded. Thank you!")
                cursor.execute("SELECT voter_Adno FROM users WHERE user_id = %s", (st.session_state.user_id, ))
                Adno = cursor.fetchone()[0]
                cursor.execute("UPDATE voters SET voting_status=1 WHERE barcode = %s", (Adno, ))
                cursor.execute("UPDATE users SET status=0 WHERE user_id = %s", (st.session_state.user_id, ))
                conn.commit()
                time.sleep(1)
                st.session_state.voting_ready = True
                st.experimental_rerun()
            else:
                st.error("⚠️ Please vote for all positions before submitting.")