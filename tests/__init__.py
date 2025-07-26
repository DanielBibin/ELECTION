import streamlit as st, mysql.connector, utils, time, voter, admin

utils.Init()
    
voter_placeholder = st.empty()
admin_placeholder = st.empty()
success_placeholder = st.empty()

st.set_page_config(page_title = 'School Election')

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "voting_ready" not in st.session_state:
    st.session_state.voting_ready = False
    
if st.session_state.voting_ready:
    voter.Voting()
    st.stop()
    

with voter_placeholder.container():
    st.header("Voter Login")
    user_id = st.text_input("Please Enter Your User ID (Max 10 characters):", value=st.session_state.user_id)
    submit_button = st.button("Submit")
    
with admin_placeholder.container():
    st.markdown("---")
    st.subheader("🔒 Admin Panel")
    admin_mode = st.checkbox("I am an Admin")
    if admin_mode:
        password = st.text_input("Enter Your Admin Password", type = "password")

if admin_mode:
    if password == 'admin123':
        with success_placeholder.container():
            st.success("Welcome Admin")
        time.sleep(.5)
        admin_placeholder.empty()
        voter_placeholder.empty()
        success_placeholder.empty()
        admin.Admin_Powers()
    elif password != "":
        st.error("Incorrect Password")
        

else:
    if submit_button and user_id.strip():
        st.session_state.user_id = user_id.strip()
    
        conn = mysql.connector.connect(host='localhost', user='root', password='12345678')
        cursor = conn.cursor()
        cursor.execute("USE Student_Election;")
        cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO users(user_id) VALUES(%s);", (user_id,))
            conn.commit()
        conn.close()
        if st.session_state.user_id:
            with success_placeholder.container():
                st.success("Successfully logged in as %s"%(user_id))
            time.sleep(0.5)
            voter_placeholder.empty()
            admin_placeholder.empty()
            success_placeholder.empty()
            voter.Voting()

