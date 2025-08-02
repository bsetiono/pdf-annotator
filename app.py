import streamlit as st
import pdfplumber
import tempfile

st.set_page_config(page_title="📄 PDF Annotator", layout="wide")

st.title("📄 PDF Annotator for SLR")
st.markdown("Upload a PDF file, read its content, and add annotations based on the research template.")

default_annotation = {
    "🌟 Key Findings": "",
    "🧪 Research Method": "",
    "📊 Important Data": "",
    "📌 Key Quotes": "",
    "❗ Criticism or Limitations": ""
}

# Upload file
uploaded_file = st.file_uploader("Upload your PDF file here", type=["pdf"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Read PDF text
    full_text = ""
    try:
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")

    # Show extracted text
    st.subheader("📖 Extracted Text")
    st.text_area("PDF Content", full_text, height=300)

    # Annotation template
    st.subheader("📝 Add Your Annotations")
    annotations = {}
    for section in default_annotation:
        annotations[section] = st.text_area(section, default_annotation[section])

    if st.button("💾 Save Annotations"):
        st.success("Annotations saved (simulation only).")
