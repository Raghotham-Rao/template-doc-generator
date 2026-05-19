import streamlit as st
import re
import sqlite3
import pandas as pd
import const
from streamlit_tree_select import tree_select
from utils.data_path import nodes
import json


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
        template_base = st.selectbox(label='Select Doc Base', options=['Shipment', 'Delivery'])

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


def show_tabular_col_mapper(flat, template_variables):
    # only leaf nodes (no children) should be selectable
    leaf_items = [item for item in flat if not item['has_children']]
    values = [item['value'] for item in leaf_items]
    display_map = {}
    for item in flat:
        icon = '📦' if item['has_children'] else '🔤'
        # mat_icon_name = 'data-object' if item['has_children'] else 'text-fields'
        display_text = f"{icon} {item['value']}"
        if item['has_children']:
            display_text = f"{display_text} — not selectable"
        display_map[item['value']] = display_text
    
    header_cols = st.columns([2, 1, 2, 3, 2])
    header_cols[0].markdown("**Template Variable**")
    header_cols[1].markdown("**Value Type**")
    header_cols[2].markdown("**Source Table**")
    header_cols[3].markdown("**Source Column / Value**")
    header_cols[4].markdown("**Additional Details**")

    for template_variable in template_variables:
        cols = st.columns([2, 1, 2, 3, 2])
        cols[0].markdown(f'##### `{template_variable}`', unsafe_allow_html=True)

        value_type = cols[1].selectbox(label='Value Type', options=['Derived', 'Static Value', 'Formula'], key=f'{template_variable}_value_type', label_visibility='collapsed')

        if value_type == 'Static Value':
            variable_value = cols[2].text_input(label='value', key=f'{template_variable}_source_selection', label_visibility="collapsed")
            formatted_variable_value = f'*{variable_value}*'
        elif value_type == 'Derived':
            variable_value = cols[2].selectbox(
                "Source Path",
                values if values else [''],
                key=f'{template_variable}_source_selection',
                format_func=lambda v, m=display_map: m.get(v, v),
                label_visibility="collapsed",
            )
            formatted_variable_value = f'`{variable_value}`'

        cols[3].markdown(formatted_variable_value)
        # selected_table = st.session_state.get(f'{template_variable}_source_table', const.DATABASE_TABLES[0])
        # columns_of_table = table_columns[selected_table]["columns"]
        # cols[2].selectbox(
        #     "Source Column",
        #     columns_of_table,
        #     key=f'{template_variable}_source_column',
        #     label_visibility="collapsed",
        # )
        # cols[3].text_input(
        #     "Additional Details",
        #     key=f'{template_variable}_additional_details',
        #     label_visibility="collapsed",
        # )


def show_bulk_editor():
    variable_map_json = dict(st.session_state)
    st.text_area('Bulk edit variable mapper', value=json.dumps(variable_map_json, indent=4))



def map_variables_tab():
    map_variables_header_cols = st.columns([10, 1])
    # map_variables_header_cols[0].markdown('### Map Variables')
    bulk_editor = map_variables_header_cols[1].checkbox('Bulk Edit')
    template_variables = [i[2:-2] for i in re.findall(r'\{\{[\w _ \d]+\}\}', st.session_state['template_html'])]
    table_columns = {}

    for table_name in const.DATABASE_TABLES:
        df = pd.read_sql(f'pragma table_info({table_name})', conn)
        table_columns[table_name] = {
            "columns": df['name'].to_list(),
            "dtype": df['type'].to_list()
        }
    
    # build flattened list of node options (value -> label) with icon markers
    def _flatten(nodes_list, prefix=None):
        out = []
        for n in nodes_list:
            has_children = 'children' in n and isinstance(n['children'], list) and len(n['children']) > 0
            part = n.get('label', n.get('value', ''))
            full = f"{prefix}.{part}" if prefix else part
            out.append({
                'label': n.get('label', ''),
                'value': full,
                'has_children': has_children
            })
            if has_children:
                out.extend(_flatten(n['children'], prefix=full))
        return out
    
    flat = _flatten(nodes)
    if not bulk_editor:
        show_tabular_col_mapper(flat, template_variables)
    else:
        show_bulk_editor()


def view_and_save_tab():
    st.header('View and save')

    return_select = tree_select(nodes)
    st.write(return_select)



tabs = st.tabs(['Create HTML Template', 'Map Variables', 'View and Save'])
with tabs[0]:
    define_html_template_tab()

with tabs[1]:
    map_variables_tab()

with tabs[2]:
    view_and_save_tab()