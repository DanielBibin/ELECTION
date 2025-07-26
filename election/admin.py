import streamlit as st, voting, register_candidate, register_voter, results, report, DBMS
from streamlit_option_menu import option_menu

class Admin_Powers:
    def __init__(self):
        st.header("Admin Panel")
        
        with st.sidebar:
            selected = option_menu("Main Menu", ["🗳️ Voting", "🧾 Register Candidate", "🆔 Register Voter", "📊 Live Results", "📑 Report Generation", "🗄️ Database Management"], default_index=0)
            
        if selected == '🗳️ Voting':
            voter = voting.Voting()
        elif selected == '🧾 Register Candidate':
            voter = register_candidate.register_c()
        elif selected == '🆔 Register Voter':
            voter = register_voter.register_v()
        elif selected == '📊 Live Results':
            voter = results.live_results()
        elif selected == '📑 Report Generation':
            voter = report.report_gen()
        elif selected == '🗄️ Database Management':
            voter = DBMS.management()