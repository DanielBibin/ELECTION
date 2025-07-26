import streamlit as st
import mysql.connector
import time
import io
from PIL import Image

class Voting:
    def __init__(self):
        # Check if already voted to prevent reloading
        if st.session_state.get("voted", False):
            return

        header_placeholder = st.empty()

        # Connect to DB
        conn = mysql.connector.connect(host='localhost', user='root', password='12345678')
        cursor = conn.cursor()
        cursor.execute("USE Student_Election;")

        # Check voting status for this user
        cursor.execute("SELECT status FROM users WHERE user_id = %s", (st.session_state.user_id,))
        result = cursor.fetchone()
        if result is None or result[0] != 1:
            header_placeholder.empty()
            with header_placeholder.container():
                st.header("❌ Voting Is Not Currently Available for this Device")
            time.sleep(2)
            st.rerun()
            return

        # Show confirmation once
        if "voting_allowed_shown" not in st.session_state:
            with header_placeholder.container():
                st.header("✅ Voting Has Been Allowed for this Device")
            time.sleep(0.5)
            st.session_state.voting_allowed_shown = True
        header_placeholder.empty()

        # Fetch positions
        cursor.execute("SELECT DISTINCT Standing_For FROM candidates")
        positions_data = cursor.fetchall()

        form_placeholder = st.empty()
        success_placeholder = st.empty()

        # Generate a form with unique key
        form_key = f"Voting_Form_{st.session_state.user_id}"
        selections = []

        with form_placeholder.form(form_key):
            for pos_row in positions_data:
                position = pos_row[0]
                st.subheader("Position: " + position)

                # Get candidates
                cursor.execute("SELECT Name, picture FROM candidates WHERE Standing_For = %s", (position,))
                candidates_data = cursor.fetchall()

                candidate_names = []
                candidate_images = []

                for candidate_row in candidates_data:
                    candidate_names.append(candidate_row[0])
                    candidate_images.append(candidate_row[1])

                # Show candidate images
                cols = st.columns(len(candidate_names))
                for i in range(len(candidate_names)):
                    image_bytes = io.BytesIO(candidate_images[i])
                    image = Image.open(image_bytes)
                    with cols[i]:
                        st.image(image, use_container_width=True)
                        st.caption(candidate_names[i])

                # Create a unique key for this radio
                radio_key = f"radio_{position}_{st.session_state.user_id}"
                selected_candidate = st.radio(
                    "Select your candidate for " + position,
                    candidate_names,
                    index=None,
                    key=radio_key
                )
                selections.append((position, selected_candidate))

            submit_button = st.form_submit_button("Submit")

        # If submitted
        if submit_button:
            incomplete_vote = False
            for position, selected_candidate in selections:
                if selected_candidate is None:
                    incomplete_vote = True
                    break

            if incomplete_vote:
                st.error("⚠️ Please vote for all positions before submitting.")
            else:
                # Submit each vote
                for position, selected_candidate in selections:
                    cursor.execute(
                        "UPDATE candidates SET votes = votes + 1 WHERE Name = %s AND Standing_For = %s",
                        (selected_candidate, position)
                    )
                conn.commit()

                # Mark the user as voted
                cursor.execute("SELECT voter_Adno FROM users WHERE user_id = %s", (st.session_state.user_id,))
                result = cursor.fetchone()
                if result:
                    adno = result[0]
                    cursor.execute("UPDATE voters SET voting_status=1 WHERE barcode = %s", (adno,))
                cursor.execute("UPDATE users SET status=0 WHERE user_id = %s", (st.session_state.user_id,))
                conn.commit()

                # Show success message
                form_placeholder.empty()
                with success_placeholder.container():
                    st.success("✅ Your votes have been recorded. Thank you!")
                time.sleep(1)
                success_placeholder.empty()

                # Clean only this user's keys
                for key in list(st.session_state.keys()):
                    if st.session_state.user_id in key or key.startswith("radio_"):
                        del st.session_state[key]

                st.session_state.voted = True  # Prevent reloading
                st.rerun()
