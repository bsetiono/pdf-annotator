import streamlit as st
import pdfplumber
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Setup halaman
st.set_page_config(page_title="PDF Annotator for SLR", layout="wide")
st.title("📄 PDF Annotator for Systematic Literature Review (SLR)")
st.markdown("Upload a PDF file, and this app will automatically generate annotations in English.")

# Template anotasi
anotasi_template = {
    "🌟 Main Findings": "",
    "🧪 Research Method": "",
    "📊 Key Data": "",
    "📌 Important Quote": "",
    "❗ Weaknesses / Critique": ""
}

# Fungsi ringkasan
def summarize_text(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

# Upload file
uploaded_file = st.file_uploader("📤 Upload PDF file", type=["pdf"])

if uploaded_file:
    full_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    if not full_text.strip():
        st.warning("⚠️ No extractable text found in the PDF.")
    else:
        if st.button("🔍 Generate Annotation Draft"):
            with st.spinner("Generating summary..."):
                summary = summarize_text(full_text)

                anotasi_template["🌟 Main Findings"] = summary
                anotasi_template["📌 Important Quote"] = summary.split(".")[0] + "..."

            st.success("✅ Draft annotation generated successfully!")
            st.subheader("📝 Annotation Draft")

            for key, value in anotasi_template.items():
                st.text_area(key, value=value, key=key)
