# Load Framework library
from traitlets.traitlets import default
import streamlit as st

# Load the pages
import exploratory_app
import forecasting_app
import about_data_app

PAGES = {
    "Exploratory Data Analysis": exploratory_app,
    'Forecasting': forecasting_app,
    'About data': about_data_app,
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()

hide_st_style = """
    <style>
        footer {visibility: hidden;}
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)