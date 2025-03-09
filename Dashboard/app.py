import streamlit as st

st.set_page_config(page_title="Job Market Analysis", layout="wide")

# Add logo at the top of the sidebar using a relative path (ideal for GitHub sharing)
st.sidebar.image("logo.jpg", width=150)
st.sidebar.title("Navigation")

from eda import eda_page
from recommendation import recommendation_page

page = st.sidebar.radio("Go to", ["📊 Job Market Analysis", "🔍 Job Recommendations"])

if page == "📊 Job Market Analysis":
    eda_page()
elif page == "🔍 Job Recommendations":
    recommendation_page()
