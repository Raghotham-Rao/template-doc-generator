import streamlit as st

st.set_page_config(layout="wide")

pages = [
    st.Page("pages/create_template.py", title='Create Template'),
    st.Page("pages/download_docs.py", title='Download Docs')
]

pg = st.navigation(pages=pages)

pg.run()

# nav_bar.page_link(page='pages/create_template.py', label='Create Template')

# if nav_option == "View templates":
#     st.title("View Templates")
#     st.write("Select a template from the list or start with one of the sample templates below.")
#     st.markdown("- Template 1: Basic HTML document\n- Template 2: Landing page\n- Template 3: Report layout")
#     st.info("This is the home view and the default option.")

# elif nav_option == "Create template":
#     st.title("Create Template")
#     st.write("Enter HTML content on the left and preview it on the right.")

#     code_section, preview_section = st.columns([0.35, 0.65])

#     with code_section:
#         html_content_input = st.text_area(
#             label="HTML Content",
#             placeholder="Enter your HTML content here",
#             height=400,
#         )

#     with preview_section:
#         if html_content_input.strip():
#             st.subheader("Preview")
#             st.write("Live preview of the HTML content below:")
#             st.components.v1.html(html_content_input, height=400, scrolling=True)
#         else:
#             st.info("Enter HTML content to see the preview.")

# else:
#     st.title("Download Docs")
#     st.write("Generate or download documentation files from your selected templates.")
#     docs_content = "Sample documentation content generated from your templates."
#     st.download_button(
#         label="Download docs",
#         data=docs_content,
#         file_name="generated_docs.txt",
#         mime="text/plain",
#     )
#     st.success("Click the button to download the docs file.")