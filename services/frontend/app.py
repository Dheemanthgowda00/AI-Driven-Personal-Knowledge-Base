import streamlit as st
import os
import sys
from dotenv import load_dotenv

from ingestion import clone_repo, index_repository
from orchestration import get_retrieval_chain, ask_question

load_dotenv()

st.set_page_config(page_title="GitChat AI", page_icon="🤖", layout="wide")

st.title("🤖 GitChat: Chat with GitHub Repos")
st.markdown("Analyze and query any public GitHub repository using AI.")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/user/repo")
    
    if st.button("🚀 Index Repository"):
        if repo_url:
            with st.status("Processing Repository...", expanded=True) as status:
                st.write("Cloning repository...")
                repo_name = repo_url.split("/")[-1].replace(".git", "")
                temp_path = os.path.join("data", "temp_repos", repo_name)
                
                try:
                    clone_repo(repo_url, temp_path)
                    st.write("Indexing files into ChromaDB...")
                    index_repository(temp_path, repo_name)
                    st.session_state.current_repo = repo_name
                    status.update(label="Indexing Complete!", state="complete", expanded=False)
                    st.success(f"Successfully indexed {repo_name}!")
                except Exception as e:
                    st.error(f"Error: {e}")
                    status.update(label="Index Failed", state="error")
        else:
            st.warning("Please enter a valid GitHub URL.")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_repo" in st.session_state:
    st.info(f"Currently chatting with: **{st.session_state.current_repo}**")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "context" in message and message["context"]:
                with st.expander("🔍 View Source Snippets"):
                    for i, snippet in enumerate(message["context"]):
                        st.code(snippet, language="python")

    # User Input
    if prompt := st.chat_input("Ask a question about the codebase..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    chain = get_retrieval_chain(st.session_state.current_repo)
                    result = ask_question(chain, prompt)
                    
                    st.markdown(result["answer"])
                    
                    if result["context"]:
                        with st.expander("🔍 View Source Snippets"):
                            for i, snippet in enumerate(result["context"]):
                                st.code(snippet, language="python")

                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": result["answer"],
                        "context": result["context"]
                    })
                except Exception as e:
                    st.error(f"Error querying Gemini: {e}")
else:
    st.write("👈 Please index a repository in the sidebar to start chatting.")

# Footer
st.divider()
st.caption("Powered by Google Gemini 1.5, LangChain, and ChromaDB.")
