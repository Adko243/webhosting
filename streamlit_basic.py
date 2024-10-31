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
st.title("Example of how we can print labels...")
html(my_html)

# Additional content
st.write("This content will be sent to the printer.")
st.write("You can customize this page with more details before printing.")
