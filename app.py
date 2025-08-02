import streamlit as st
import pdfplumber
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer  # Anda bisa ganti dengan LexRankSummarizer

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="PDF Annotator for SLR", layout="wide")

# Judul dan deskripsi
st.title("📄 PDF Annotator for SLR")
st.markdown("Upload a PDF file, read its content, and add annotations based on the research template.")

# Template anotasi
ANOTASI_TEMPLATE = {
    "🌟 Temuan utama": "",
    "🧪 Metode penelitian": "",
    "📊 Data penting": "",
    "📌 Kutipan kunci": "",
    "❗ Kritik/kekurangan": ""
}

# Fungsi ringkasan
def summarize_text(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

# Upload file
uploaded_file = st.file_uploader("Upload your PDF file here", type="pdf")

if uploaded_file:
    all_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"

    if all_text.strip() == "":
        st.warning("⚠️ Tidak ada teks yang berhasil diekstrak dari file PDF.")
    else:
        st.subheader("📃 Extracted Text")
        st.text_area("PDF Text Content", all_text, height=300)

        if st.button("🛠 Generate Annotation Draft"):
            summary = summarize_text(all_text)

            ANOTASI_TEMPLATE["🌟 Temuan utama"] = summary
            ANOTASI_TEMPLATE["📌 Kutipan kunci"] = summary.split(".")[0] + "..."  # Ambil kalimat pertama

            st.subheader("📝 Annotation Draft")
            for key, value in ANOTASI_TEMPLATE.items():
                st.text_area(label=key, value=value, key=key)
