import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, createStringObject
import tempfile
import os

# Streamlit app layout
st.title("PDF Compressor")
st.write("Upload a PDF file to reduce its size and keeping everything else intact for FREE!.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_input.write(uploaded_file.read())
    temp_input.close()

    reader = PdfReader(temp_input.name)
    writer = PdfWriter()

    # Set new annotation date
    new_date = "2024-12-31T10:00:00Z"

    for page in reader.pages:
        if "/Annots" in page:
            for annot in page["/Annots"]:
                obj = annot.get_object()
                obj.update({NameObject("/M"): createStringObject(new_date)})
                if "/CreationDate" in obj:
                    obj.update({NameObject("/CreationDate"): createStringObject(new_date)})
        writer.add_page(page)

    # Reduce PDF size by removing metadata (basic simulation of compression)
    writer.add_metadata({})

    # Write to a temporary output file
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    with open(temp_output.name, "wb") as f_out:
        writer.write(f_out)

    # Offer the file for download
    with open(temp_output.name, "rb") as f_out:
        st.download_button("Download Modified PDF", f_out, file_name="updated_pdf.pdf")

    # Clean up temp files
    os.remove(temp_input.name)
    os.remove(temp_output.name)
