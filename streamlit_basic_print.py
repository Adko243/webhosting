import streamlit as st
from streamlit.components.v1 import html

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
st.title("MR sistemas label printer v1")

# New input field
user_input = st.text_input("Enter input for printing:")

# Display the input in a div
st.write(f"Printing this: {user_input}")

# Add the print button and content to print
html(f"""
<div id="content-to-print">
    <p>{user_input}</p>
</div>
{my_html}
""")

# Additional content
st.write("This content will be sent to the printer.")

