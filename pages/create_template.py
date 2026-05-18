import streamlit as st
import re
import sqlite3
import pandas as pd
import const


conn = sqlite3.connect('transport_doc_generator.db')


st.title("Create Template")


@st.dialog("View Doc Full Screen", width="large", icon=":material/fullscreen:")
def view_template_fullscreen(html_content):
    st.iframe(html_content)


def define_html_template_tab():
    code_section, preview_section = st.columns([0.35, 0.65])

    with code_section:
        fields_cols = st.columns(2)
        template_name = fields_cols[0].text_input(label="Template Name", placeholder="Enter the template name")
        template_description = fields_cols[1].text_input(label="Template Description", placeholder="Add a short description to your template")

        html_content_input = st.text_area(
            label="HTML Content",
            placeholder="Enter your HTML content here",
            height=450,
        )

        st.session_state['template_html'] = html_content_input
        st.session_state['template_name'] = template_name
        st.session_state['template_description'] = template_description

    with preview_section:
        if html_content_input.strip():
            # st.subheader("Preview")
            line = st.columns([0.7, 0.1, 0.2])
            line[0].markdown("<strong>Live preview</strong>", unsafe_allow_html=True)
            line[2].button('View Fullscreen', icon=':material/fullscreen:', on_click=view_template_fullscreen, args=[html_content_input], type="tertiary")
            st.components.v1.html(html_content_input, height=480, scrolling=True)

            # st.iframe(html_content_input, height=800, scrolling=True)
        else:
            st.info("Enter HTML content to see the preview.")

    footer_columns = st.columns(7)


def map_variables_tab():
    st.header('Map Variables')
    template_variables = [i[2:-2] for i in re.findall(r'\{\{[\w _ \d]+\}\}', st.session_state['template_html'])]
    table_columns = {}

    for table_name in const.DATABASE_TABLES:
        df = pd.read_sql(f'pragma table_info({table_name})', conn)
        table_columns[table_name] = {
            "columns": df['name'].to_list(),
            "dtype": df['type'].to_list()
        }
    
    header_cols = st.columns([2, 2, 2, 2])
    header_cols[0].markdown("**Template Variable**")
    header_cols[1].markdown("**Source Table**")
    header_cols[2].markdown("**Source Column**")
    header_cols[3].markdown("**Additional Details**")

    for template_variable in template_variables:
        cols = st.columns([2, 2, 2, 2])
        cols[0].markdown(f'##### `{template_variable}`', unsafe_allow_html=True)
        cols[1].selectbox(
            "Source Table",
            const.DATABASE_TABLES,
            key=f'{template_variable}_source_table',
            label_visibility="collapsed",
        )
        selected_table = st.session_state.get(f'{template_variable}_source_table', const.DATABASE_TABLES[0])
        columns_of_table = table_columns[selected_table]["columns"]
        cols[2].selectbox(
            "Source Column",
            columns_of_table,
            key=f'{template_variable}_source_column',
            label_visibility="collapsed",
        )
        cols[3].text_input(
            "Additional Details",
            key=f'{template_variable}_additional_details',
            label_visibility="collapsed",
        )


def view_and_save_tab():
    st.header('View and save')



tabs = st.tabs(['Create HTML Template', 'Map Variables', 'View and Save'])
with tabs[0]:
    define_html_template_tab()

with tabs[1]:
    map_variables_tab()

with tabs[2]:
    view_and_save_tab()