import streamlit as st
import os
import const
from db.initial_db_setup import database_setup
from db.initial_db_load import seed_data_load

st.set_page_config(layout="wide")

if not os.path.exists(const.DB_PATH):
    os.makedirs('/'.join(const.DB_PATH.split('/')[:-1]))
    database_setup(const.DB_PATH)
    seed_data_load(const.DB_PATH)
    st.toast('Database setup succesful!', icon=':material/done_outline:')
else:
    st.toast('Database already setup!', icon=':material/done_outline:')


pages = [
    st.Page("pages/create_template.py", title='Create Template'),
    st.Page("pages/download_docs.py", title='Download Docs'),
    st.Page("pages/view_pdf.py", title='View PDF'),
]

pg = st.navigation(pages=pages)

pg.run()