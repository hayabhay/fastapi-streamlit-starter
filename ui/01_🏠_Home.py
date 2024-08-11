import httpx
import streamlit as st
from config import DEV, get_page_config, init_session

# Set up page config & init session
st.set_page_config(**get_page_config())
init_session(st.session_state)

# Render session state if in dev mode
if DEV:
    with st.sidebar.expander("Session state"):
        st.write(st.session_state)

# Render an option to change the server location
st.session_state.SERVER_LOC = st.sidebar.text_input(
    "FastAPI server location", st.session_state.SERVER_LOC
)


# Aliases for readability
# --------------------------------


st.write("### 🏠 Home")
st.write("---")

# Hit the FastAPI backend and get the openapi schema
# --------------------------------
with st.spinner("Loading FastAPI backend..."):
    response = httpx.get(f"{st.session_state.SERVER_LOC.strip("/")}/openapi.json")
    schema = response.json()

    with st.expander("FastAPI raw `openapi.json`"):
        st.write(schema)

    st.write("---")
st.write("##### Add interactive widgets & custom rendering here.")
