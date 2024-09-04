# pylint: disable=no-member
from datetime import datetime

import streamlit as st

st.set_page_config(layout="wide")

# Navigation setup
pg = st.navigation(
    [
        st.Page("home_page.py", title="About", icon="🧑‍🧑‍🧒‍🧒"),
        st.Page(
            "customer_profile.py", title="Customer Profiling Toolkit", icon="🪪"
        ),
        st.Page("file_upload.py", title="Batch Analysis Toolkit", icon="⛓️"),
    ]
)

# Copyright section
current_year = datetime.now().year
st.sidebar.markdown(
    f"""
    <div>
        <br><br><br><br><br><br>
        <b>© {current_year} Midega George</b>
    </div>
    """,
    unsafe_allow_html=True,
)

pg.run()
