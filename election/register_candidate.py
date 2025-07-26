import streamlit as st
import mysql.connector
import time

class register_c:
    def __init__(self):
        if "show_modal" not in st.session_state:
            st.session_state.show_modal = False
        if "position_value" not in st.session_state:
            st.session_state.position_value = None
        if "form_submitted" not in st.session_state:
            st.session_state.form_submitted = False

        st.subheader("Registering A New Candidate")

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='12345678',
            database='student_election'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT Standing_For FROM candidates;")
        result = cursor.fetchall()

        positions = []
        if result is not None:
            for pos in result:
                positions.append(pos[0])

        form = st.form("Registering Candidate", clear_on_submit=False)
        with form:
            Adno = st.text_input("Please Enter The Candidates Admission Number:")
            Name = st.text_input("Please Enter The Candidates Name:")
            Symbol = st.text_input("Please Enter The Symbol Of The Candidate:")
            position = st.selectbox("Please Select The Candidates Position:",
                positions + ["Add New Position(A Pop Up will be displayed later)"],
                index=None
            )
            picture_files = st.file_uploader("Please Input An Image Of The Candidate:", type=["jpg", "jpeg", "png", "webp"])
            col1, col2, col3, col4, col5 = st.columns(5)
            with col3:
                submit = st.form_submit_button("Submit")

        if submit:
            st.session_state.form_submitted = True
            if position == "Add New Position(A Pop Up will be displayed later)":
                st.session_state.show_modal = True
            else:
                st.session_state.position_value = position

        if st.session_state.show_modal:
            with st.modal("Enter New Position:"):
                newposition = st.text_input("Enter The New Position")
                col1, col2, col3 = st.columns(3)
                with col2:
                    modal_submit = st.button("Submit")
                if modal_submit:
                    if newposition.strip():
                        st.session_state.position_value = newposition
                        st.session_state.show_modal = False
                        st.rerun()
                    else:
                        st.error("Please Enter The New Position")

        if (
            st.session_state.position_value
            and st.session_state.form_submitted
            and not st.session_state.show_modal
        ):
            if Adno and Name and Symbol and picture_files:
                cursor.execute("SELECT Adno FROM candidates WHERE Adno = %s", (Adno,))
                exists = cursor.fetchone()
                if exists is None:
                    picture_bytes = picture_files.read()
                    cursor.execute(
                        "INSERT INTO candidates(Adno, Name, Symbol, Standing_For, picture) VALUES (%s, %s, %s, %s, %s);",
                        (Adno, Name, Symbol, st.session_state.position_value, picture_bytes)
                    )
                    conn.commit()
                    st.success("Successfully Entered The Candidate")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("This Candidate's Record Already Exists!")
            else:
                st.error("Please Fill All The Fields")