import streamlit as st

st.title('Home')
move = st.button("move to next page")
if move:
    st.switch_page("pages/Assets_Page.py")
