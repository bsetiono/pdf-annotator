import streamlit as st
import pdfplumber
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer  # Anda bisa ganti dengan LexRankSummarizer jika mau

st.set_page_config(page_title="PDF Annotator for SLR", layout="wide")

st.title("📄 PDF Annotator for SLR")
st.markdown("Upload a PDF file, read its content, and add annotations based on the research template.")

uploaded_file = st.file_uploader("Upload your PDF file here", type="pdf")

ANOTASI_TEMPLATE = {
    "🌟 Temuan utama": "",
    "🧪 Metode penelitian": "",
    "📊 Data penting": "",
    "📌 Kutipan kunci": "",
    "❗ Kritik/kekurangan": ""
}

def summarize_text(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text() or ""

    st.subheader("📃 Extracted Text")
    st.text_area("PDF Text Content", all_text, height=300)

    if st.button("Generate Annotation Draft"):
        summary = summarize_text(all_text)

        ANOTASI_TEMPLATE["🌟 Temuan utama"] = summary
        ANOTASI_TEMPLATE["📌 Kutipan kunci"] = summary

        st.subheader("📝 Annotation Draft")
        for key, value in ANOTASI_TEMPLATE.items():
            st.text_area(key, value, key)
