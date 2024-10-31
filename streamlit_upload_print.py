import streamlit as st
from streamlit.components.v1 import html
import base64

# JavaScript to open the print dialog
my_js = """
    window.onload = function() {
        const printButton = document.getElementById('print-button');
        printButton.onclick = function() {
            window.print();
        };
    };
"""

# Wrap the JavaScript in HTML
my_html = f"""
<div>
    <button id="print-button">Print</button>
</div>
<script>{my_js}</script>
"""

# Execute your app
st.title("Example of how we can print labels...")

# Upload text file
uploaded_file = st.file_uploader("Choose a text file", type=["txt"])

# Initialize variable to store file content
file_content = ""

if uploaded_file is not None:
    # Read the file content
    file_content = uploaded_file.read().decode("utf-8")

# Display the file content in the text input field
user_input = st.text_area("File content:", file_content)

# Sidebar for the image
st.sidebar.title("Upload Image")
uploaded_image = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

image_display = ""
if uploaded_image is not None:
    encoded_image = base64.b64encode(uploaded_image.read()).decode()
    image_display = f'<img src="data:image/jpeg;base64,{encoded_image}" style="max-width:100%;">'

# Add the print button and content to print
html(f"""
<div>
    {my_html}
</div>
<div id="content-to-print">
    <p>{user_input}</p>
    {image_display}
</div>
""")

# Additional content
st.write("This content will be sent to the printer.")
st.write("You can customize this page with more details before printing.")
