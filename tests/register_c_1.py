import streamlit as st, mysql.connector, time

class register_c:
    def __init__(self):
        st.subheader("Registering A New Candidate")
        conn = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '12345678', database = 'student_election')
        cursor = conn.cursor()
        positions = []
        cursor.execute("SELECT Standing_For FROM candidates;")
        result = cursor.fetchall()
        if result is not None:
            for position in result:
                positions.append(position[0])
        registering_c_from = st.form("Registering Candidate", True)
        with registering_c_from:
            Adno = st.text_input("Please Enter The Candidates Admission Number: ")
            Name = st.text_input("Please Enter The Candidates Name: ")
            Symbol = st.text_input("Please Enter The Symbol Of The Candidate: ")
            position = st.selectbox("Please Select The Candidates Position: ", positions + ["Add New Position"], index = None)
            picture_files = st.file_uploader("Please Input An Image Of The Candidate: ", type = ['jpg', 'jpeg', 'png', 'webp'])
            col1, col2, col3, col4, col5 = st.columns(5)
            with col3:
                global submit
                submit = st.form_submit_button()
            if position == 'Add New Position':
                new_position = st.text_input("Enter the New Position")
                st.rerun()
                if new_position is not None:
                    position = new_position
                else:
                    position = None
            if submit:
                if Adno is not None or Name is not None or Symbol is not None or position is not None or picture_files is not None:
                    cursor.execute("SELECT Adno FROM candidates WHERE Adno = %s", (Adno,))
                    result = cursor.fetchone()
                    if result is None:
                        picture_bytes = picture_files.read()
                        cursor.execute("INSERT INTO candidates(Adno, Name, Symbol, Standing_For, picture) VALUES(%s, %s,%s,%s,%s);", (Adno, Name, Symbol, position, picture_bytes))
                        conn.commit()
                        st.success("Successfully Entered The Candidate")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("This Candidate's Record Already Exists!")
                else:
                    st.error("Please Fill All The Fields")