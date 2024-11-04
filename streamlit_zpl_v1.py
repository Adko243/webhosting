import streamlit as st
import socket
import base64
from streamlit.components.v1 import html

zpl_data = """
^XA
^FO50,50^ADN,36,20^FDHello, World!^FS
^XZ
"""

def create_zpl_label(text):
    zpl = f""" ^XA ^FO50,50^ADN,36,20^FD{text}^FS ^XZ """
    return zpl

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

# Function to send ZPL to the printer
def send_zpl_to_printer(zpl_data, printer_ip, printer_port=9100):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((printer_ip, printer_port))
            s.sendall(zpl_data.encode('utf-8'))
            st.success(f"ZPL data sent to printer at {printer_ip}:{printer_port}")
    except Exception as e:
        st.error(f"Failed to send ZPL data: {e}")

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


# Additional content
st.write("This content will be sent to the printer.")
st.write("You can customize this page with more details before printing.")

# Printer configuration
st.sidebar.title("Printer Configuration")
printer_ip = st.sidebar.text_input("Printer IP", "192.168.1.11")
printer_port = st.sidebar.number_input("Printer Port", value=9100)

if st.button("Send to Printer"):
    #zpl_data = user_input  # Or construct your ZPL data as needed
    #zpl_data = create_zpl_label(user_input)
    send_zpl_to_printer(zpl_data, printer_ip, printer_port)
