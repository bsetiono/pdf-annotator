import streamlit as st
import pdfplumber
from transformers import pipeline
import tempfile
import os

# Template anotasi
ANNOTATION_TEMPLATE = {
    "🌟 Main Findings": "",
    "🧪 Research Method": "",
    "📊 Key Data": "",
    "📌 Key Quotes": "",
    "❗Criticism/Weaknesses": ""
}

# Streamlit app
st.set_page_config(page_title="PDF Annotator for SLR", layout="wide")
st.title("📄 PDF Annotator for SLR")

uploaded_file = st.file_uploader("Upload your PDF file here", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.success("✅ File uploaded successfully.")

    # Extract text from PDF
    all_text = ""
    with pdfplumber.open(tmp_path) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() or ""

    if all_text.strip() == "":
        st.warning("⚠ No text found in the PDF.")
    else:
        # Summarize with transformers
        st.subheader("🧠 AI-generated Summary")
        with st.spinner("Generating summary..."):
            summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
            # Transformer has max token limit — split if needed
            chunks = [all_text[i:i+1000] for i in range(0, len(all_text), 1000)]
            summaries = [summarizer(chunk, max_length=100, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks[:3]]  # Max 3 chunks
            full_summary = " ".join(summaries)
            st.write(full_summary)

        # Annotation input
        st.subheader("📝 Add your annotations")
        annotations = {}
        for key in ANNOTATION_TEMPLATE:
            annotations[key] = st.text_area(key, value=ANNOTATION_TEMPLATE[key])

        if st.button("Save annotations"):
            st.success("✅ Annotations saved (feature to download coming soon).")
