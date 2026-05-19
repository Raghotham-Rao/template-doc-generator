import os
import sqlite3

import pandas as pd
import streamlit as st

import const


def get_db_path() -> str:
    base_dir = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(base_dir, '..', const.DB_PATH))


def load_table(table_name: str, conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql_query(f'SELECT * FROM {table_name}', conn)


st.title('View PDF / Database Tables')

try:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)

    st.markdown('This page shows all database tables as Streamlit dataframes.')

    for table_name in const.DATABASE_TABLES:
        with st.expander(f'Table: {table_name}', expanded=False):
            df = load_table(table_name, conn)
            if df.empty:
                st.info('No rows found in this table.')
            else:
                st.caption(f'{len(df)} row(s) in table `{table_name}`')
                st.dataframe(df)

    conn.close()
except Exception as exc:
    st.error(f'Unable to load tables: {exc}')
