import streamlit as st, mysql.connector, time, utils, voter, admin

utils.Init()

st.set_page_config(page_title="School Election", layout = 'centered')

if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if st.session_state.user_id:
    if st.session_state.is_admin:
        admin.Admin_Powers()
    else:
        voter.Voting()
    st.stop()

login_placeholder = st.empty()
admin_placeholder = st.empty()
status_placeholder = st.empty()

with login_placeholder.container():
    st.markdown("## 🗳️ Voter Login")
    user_id = st.text_input("Enter Your User ID (Max 10 characters):", value=st.session_state.user_id)
    login_button = st.button("Login")

with admin_placeholder.container():
    st.markdown("---")
    st.markdown("### 🔐 Admin Panel")
    admin_mode = st.checkbox("I am an Admin")
    if admin_mode:
        password = st.text_input("Admin Password", type="password")
        admin_button = st.button("Access Admin Panel")

if admin_mode and admin_button:
    if password == "admin123":
        st.session_state.user_id = "admin"
        st.session_state.is_admin = True
        admin_placeholder.empty()
        login_placeholder.empty()
        status_placeholder.success("✅ Welcome Admin")
        time.sleep(0.5)
        st.rerun()
    else:
        status_placeholder.error("❌ Incorrect admin password")

if login_button and user_id.strip():
    user_id = user_id.strip()
    conn = mysql.connector.connect(host='localhost', user='root', password='12345678')
    cursor = conn.cursor()
    cursor.execute("USE Student_Election")
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO users(user_id) VALUES(%s)", (user_id,))
        conn.commit()
    conn.close()

    st.session_state.user_id = user_id
    st.session_state.is_admin = False
    admin_placeholder.empty()
    st.rerun()
