import streamlit as st
import vote_chain
import app
import json

def authenticate_admin(username, password):
    return username == "admin" and password == "admin123"

st.set_page_config(
    page_title="Blockchain-based Voting System",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

is_admin_logged_in = st.session_state.get("is_admin_logged_in", False)  

st.title("Blockchain-based Voting System")

if not is_admin_logged_in:
    st.sidebar.title("Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if authenticate_admin(username, password):
            st.session_state["is_admin_logged_in"] = True
            is_admin_logged_in = True
        else:
            st.sidebar.error("Invalid username or password")

if is_admin_logged_in:
    st.sidebar.header("Admin Interface")
    
    # Add Candidate Section
    st.sidebar.subheader("Add Candidate")
    new_candidate = st.sidebar.text_input("New Candidate Name:")
    if st.sidebar.button("Add Candidate"):
        new_candidate = new_candidate.strip()
        if new_candidate:
            vote_chain.candidates.append(new_candidate)
            st.sidebar.success(f"Added candidate -> {new_candidate} successfully.")
        else:
            st.sidebar.warning("Please enter a valid candidate name.")
    
    st.sidebar.subheader("Remove Candidate")
    candidate_to_remove = st.sidebar.selectbox("Select Candidate to Remove:", vote_chain.candidates)
    if st.sidebar.button("Remove Candidate"):
        vote_chain.candidates.remove(candidate_to_remove)
        st.sidebar.success(f"Removed candidate -> {candidate_to_remove} successfully.")

else:
    st.header("User Interface")
    voter_name = st.text_input("Voter Name")
    option_list = [_ for _ in vote_chain.candidates]
    voter_choose = st.selectbox("Choose your candidate to vote for", option_list)
    voter_key = st.text_input("Voter Key")

    if st.button("Vote"):
        new_voter = vote_chain.Voter(voter_name, vote_chain.voter_code)
        voter_identifier = voter_key
        if voter_identifier in app.israel_election.previouslyVoted:
            st.error("Error: You can only vote once!")
        else:
            new_vote = vote_chain.Vote(new_voter.key, voter_choose)
            app.israel_election.create_block(new_vote, voter_name, voter_key)
            st.success(f"Voted for -> {voter_choose}")
            
    with open("vote_count.json") as infile:
        vote_count_with_timestamp = json.load(infile)
        vote_count = vote_count_with_timestamp["vote_count"]

    st.subheader("Vote Count")
    vote_count = app.israel_election.get_votes()
    for candidate, count in vote_count.items():
        st.write(f"{candidate}: {count}")