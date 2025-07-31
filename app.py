import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
from langdetect import detect
import spacy

pytesseract.pytesseract.tesseract_cmd =  r"C:\Users\Shikhar\Downloads\tesseract-ocr-w64-setup-5.5.0.20241111.exe"

# Load API keys and models
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
nlp = spacy.load("en_core_web_sm")

# Utility Functions
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)


def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def classify_document(text):
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in ["contract", "court", "affidavit"]):
        return "Legal"
    elif any(keyword in text_lower for keyword in ["loan", "bank", "investment"]):
        return "Finance"
    elif any(keyword in text_lower for keyword in ["patient", "diagnosis", "treatment"]):
        return "Healthcare"
    else:
        return "General"

# Streamlit App
st.set_page_config(page_title="GeminiDecode", layout="wide")
st.title("📄 GeminiDecode: Multilanguage Document Extraction")

uploaded_file = st.file_uploader("Upload a document (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    if file_ext in ["png", "jpg", "jpeg"]:
        image = Image.open(uploaded_file)
        text = extract_text_from_image(image)
    elif file_ext == "pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        st.error("Unsupported file type.")
        st.stop()

    language = detect_language(text)
    doc_type = classify_document(text)

    st.subheader("📌 Document Metadata")
    st.write(f"**Detected Language:** {language}")
    st.write(f"**Document Type:** {doc_type}")

    st.subheader("📝 Extracted Text")
    st.text_area("Full Text", text, height=300)