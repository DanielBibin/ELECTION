import streamlit as st, mysql.connector

class Voting:
    def __init__(self):
        conn = mysql.connector.connect(host = 'localhost', user = 'root', password = '12345678', database = 'student_election')
        cursor = conn.cursor()
        st.subheader("Voting")
        Voting_Form = st.form("Voting Form", True)
        with Voting_Form:
            users = []
            Adno = st.text_input("Click in to this and scan barcode on ID Card")
            cursor.execute("SELECT user_id FROM users;")
            result = cursor.fetchall()
            if result is not None:
                for user in result:
                    users.append(user[0])
            user_id = st.multiselect("Enter the user ID of the target PC", users)
            submit = st.form_submit_button()
            if submit:
                st.write(users)
            