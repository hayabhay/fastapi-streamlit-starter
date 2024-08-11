import streamlit as st
from config import get_page_config, init_session

# Set up page config & init session
st.set_page_config(**get_page_config())
init_session(st.session_state)

st.write("### 🗒️ About")
st.write("---")
st.write("This is a simple Streamlit app to interface with a FastAPI backend.")
