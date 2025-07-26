import streamlit as st, mysql.connector, time

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
            user_id = st.selectbox("Enter the user ID of the target PC", users, index = None)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col3:
                global submit
                submit = st.form_submit_button()
            if submit:
                if user_id is not None and Adno is not None:
                    cursor.execute("SELECT voting_status FROM voters WHERE barcode = %s", (Adno, ))
                    result = cursor.fetchone()[0]
                    if result != 1:
                        cursor.execute("UPDATE users SET status = 1, voter_adno = %s WHERE user_id = %s", (Adno, user_id))
                        conn.commit()
                        st.success("Successfully gave permission to user ID "+str(user_id))
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("This Student Has Already Voted!")
                        return
                else:
                    st.error("PLease Fill All Fields!")
                    return
            