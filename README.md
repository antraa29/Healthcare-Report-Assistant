# 🩺 Healthcare Report Assistant

An AI-powered healthcare report analysis application that extracts laboratory information from PDF reports, classifies test results using configurable reference ranges, retrieves relevant medical information using RAG, and generates an easy-to-understand AI summary.

## 🚀 Overview

Healthcare Report Assistant allows users to upload a medical/laboratory report in PDF format and automatically:

1. Extract text from the PDF
2. Identify patient information and laboratory values
3. Classify laboratory results as **LOW, NORMAL, HIGH, or UNKNOWN**
4. Retrieve relevant information from a medical knowledge base using **FAISS + RAG**
5. Generate a natural-language summary using **Google Gemini**
6. Display the results through an interactive **Streamlit dashboard**
7. Provide the analysis through a **FastAPI REST API**

The application is designed as an end-to-end AI pipeline combining document processing, information extraction, retrieval-augmented generation, and LLM-based summarization.

---

## ✨ Features

### 📄 PDF Report Processing
- Upload healthcare/laboratory reports in PDF format
- Extract text automatically from uploaded reports
- Temporary file handling for uploaded reports

### 🔍 Patient & Laboratory Data Extraction
Extracts information such as:

- Patient Name
- Age / Gender
- HbA1c
- Fasting Blood Sugar
- Uric Acid
- Vitamin D
- Vitamin B12
- Prolactin
- TSH

The extraction pipeline can be extended to support additional laboratory tests.

### 📊 Deterministic Lab Classification

Laboratory values are evaluated using configurable reference ranges rather than relying only on the LLM.

Each result can be classified as:

- 🟢 NORMAL
- 🔴 LOW
- 🔴 HIGH
- ⚪ UNKNOWN

Reference information such as units and expected ranges is also displayed.

### 🧠 Retrieval-Augmented Generation

The application uses a RAG pipeline to retrieve relevant information from a medical knowledge base.

**Pipeline:**

```text
Medical Knowledge Base
        ↓
Document Embeddings
        ↓
FAISS Vector Store
        ↓
Similarity Search
        ↓
Relevant Medical Context
        ↓
Gemini LLM
