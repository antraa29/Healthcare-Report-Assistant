# 🩺 Healthcare Report Assistant

An AI-powered healthcare report analysis application that extracts patient and laboratory information from PDF reports, evaluates laboratory values against configurable reference ranges, retrieves relevant medical context using Retrieval-Augmented Generation (RAG), and generates an easy-to-understand AI summary using Google Gemini.

## 🚀 Overview

Healthcare Report Assistant is an end-to-end AI application designed to simplify the analysis of laboratory reports.

The system combines:

- 📄 PDF text extraction
- 🔎 Pattern-based information extraction
- 📊 Deterministic laboratory classification
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 FAISS vector search
- 🤖 Google Gemini
- ⚡ FastAPI
- 🎨 Streamlit

### Workflow

```text
PDF Healthcare Report
        ↓
PDF Text Extraction
        ↓
Patient & Lab Data Extraction
        ↓
Reference Range Classification
        ↓
RAG Context Retrieval
        ↓
Google Gemini
        ↓
AI-Generated Summary
        ↓
Streamlit Dashboard
```

---

## ✨ Features

### 📄 PDF Report Processing

- Upload healthcare reports in PDF format
- Extract readable text from reports
- Process reports through a FastAPI backend
- Temporarily store uploaded reports during processing
- Automatically remove temporary files after processing

### 👤 Patient Information Extraction

The application extracts:

- Patient Name
- Age / Gender

### 🧪 Laboratory Data Extraction

Currently supported laboratory values include:

- HbA1c
- Fasting Blood Sugar
- Uric Acid
- Vitamin D
- Vitamin B12
- Prolactin
- TSH

The extraction pipeline can be extended to support additional laboratory tests.

### 📊 Laboratory Classification

Extracted laboratory values are compared against configured reference ranges.

Each value can be classified as:

- `LOW`
- `NORMAL`
- `HIGH`
- `UNKNOWN`

The application also provides:

- Measured value
- Unit
- Reference range
- Status

Example:

```text
Vitamin D
Value: 16.96 ng/mL
Reference: >= 20
Status: LOW
```

---

## 🧠 Retrieval-Augmented Generation

The project uses Retrieval-Augmented Generation to provide relevant medical reference information to the language model.

### RAG Pipeline

```text
Medical Knowledge Base
        ↓
Document Processing
        ↓
Embeddings
        ↓
FAISS Vector Store
        ↓
Similarity Search
        ↓
Relevant Medical Context
        ↓
Gemini
```

For each extracted laboratory test, relevant information is retrieved from the medical knowledge base and provided to Gemini as grounding context.

This helps the model generate explanations based on the retrieved reference information rather than relying only on its general knowledge.

---

## 🤖 AI Medical Summary

Google Gemini generates a natural-language explanation of the laboratory results.

The generated summary includes:

1. Overall summary
2. Normal values
3. Abnormal values
4. Possible health concerns
5. General lifestyle recommendations

The model is instructed to:

- Explain results in simple language
- Use the retrieved reference context
- Avoid providing a medical diagnosis
- Provide general informational guidance

---

## ⚡ FastAPI Backend

The project provides a REST API for healthcare report analysis.

### API Endpoints

#### `GET /`

Returns basic API information.

Example:

```json
{
  "message": "Healthcare Report Assistant API is running",
  "version": "1.0.0"
}
```

#### `GET /api/health`

Health-check endpoint.

Example response:

```json
{
  "status": "healthy"
}
```

#### `POST /api/reports/analyze`

Accepts a healthcare report PDF and returns:

- Extracted patient information
- Laboratory values
- Laboratory classification
- AI-generated summary

Example response structure:

```json
{
  "success": true,
  "patient_data": {},
  "lab_analysis": {},
  "summary": "AI-generated healthcare report summary"
}
```

---

## 🎨 Streamlit Frontend

The Streamlit application provides an interactive dashboard for users.

### Dashboard Features

- 📤 PDF upload
- 👤 Patient information display
- 🧪 Laboratory results table
- 📊 Test values
- 📏 Reference ranges
- 🟢 Normal results
- 🟡 Low results
- 🔴 High results
- 📈 Result overview
- 🤖 AI-generated medical summary
- 📥 Downloadable summary

### Result Overview

The dashboard displays the number of:

```text
Normal Results
Low Results
High Results
Unknown Results
```

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   PDF Lab Report    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   PDF Text Parser   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Data Extraction    │
                    │ Patient + Lab Data  │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐       ┌──────────────────┐
       │ Lab Classification│       │    FAISS / RAG   │
       │ LOW/NORMAL/HIGH  │       │Context Retrieval │
       └────────┬─────────┘       └────────┬─────────┘
                │                          │
                └─────────────┬────────────┘
                              ▼
                    ┌─────────────────────┐
                    │     Gemini LLM      │
                    │  AI Summarization   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Dashboard │
                    └─────────────────────┘
```

---

## 🛠️ Tech Stack

### Programming Language

- Python 3.11

### Generative AI / LLM

- Google Gemini
- LangChain
- Retrieval-Augmented Generation (RAG)

### Vector Search

- FAISS
- Embeddings

### Backend

- FastAPI
- Uvicorn
- Pydantic

### Frontend

- Streamlit
- Pandas

### Document Processing

- PDF text extraction
- Regular Expressions

### Configuration

- python-dotenv
- Environment variables

### Package Management

- uv

### Development Tools

- Git
- GitHub
- VS Code

---

## 📁 Project Structure

```text
Healthcare-Report-Assistant/
│
├── agents/
│   └── workflow.py
│
├── backend/
│   └── api.py
│
├── data/
│   └── reports/
│
├── extraction/
│   ├── extractor.py
│   └── lab_ranges.py
│
├── frontend/
│   └── streamlit_app.py
│
├── knowledge_base/
│   └── lab_reference.txt
│
├── llm/
│   └── summarizer.py
│
├── ocr/
│   ├── image_parser.py
│   └── pdf_parser.py
│
├── rag/
│   ├── qa_chain.py
│   ├── summarizer.py
│   └── vector_store.py
│
├── utils/
│
├── app.py
├── main.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

---

## 🔍 Core Components

### `backend/api.py`

Handles the FastAPI application and report-analysis endpoint.

Responsibilities:

- API routing
- PDF upload handling
- Temporary file management
- Calling the report-processing pipeline
- Returning structured JSON responses
- Error handling

### `extraction/extractor.py`

Responsible for:

- Extracting patient information
- Extracting laboratory values
- Converting laboratory values to numeric data
- Performing deterministic laboratory classification

### `extraction/lab_ranges.py`

Contains configurable reference ranges and classification logic for supported laboratory tests.

### `ocr/pdf_parser.py`

Responsible for extracting readable text from uploaded PDF reports.

### `rag/vector_store.py`

Manages the vector store used for similarity-based retrieval.

### `rag/qa_chain.py`

Retrieves relevant medical reference information for extracted laboratory tests.

### `llm/summarizer.py`

Combines:

- Extracted patient data
- Retrieved medical context
- Google Gemini

to generate the final report summary.

### `frontend/streamlit_app.py`

Provides the user-facing Streamlit dashboard and communicates with the FastAPI backend.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/antraa29/Healthcare-Report-Assistant.git
```

```bash
cd Healthcare-Report-Assistant
```

### 2. Install dependencies

The project uses `uv` for dependency management.

```bash
uv sync
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Do not commit your `.env` file or API key to GitHub.

---

## ▶️ Running the Application

The application consists of two components: a FastAPI backend and a Streamlit frontend.

### Terminal 1 — Start FastAPI Backend

```bash
uv run uvicorn backend.api:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/api/health
```

### Terminal 2 — Start Streamlit Frontend

Open a second terminal and activate the project environment if required.

```bash
cd Healthcare-Report-Assistant
```

Then run:

```bash
uv run streamlit run frontend/streamlit_app.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open the URL in your browser and upload a healthcare PDF report.

---

## 🔄 End-to-End Workflow

```text
1. User uploads a PDF
           ↓
2. Streamlit sends PDF to FastAPI
           ↓
3. FastAPI temporarily stores the file
           ↓
4. PDF text is extracted
           ↓
5. Patient information is extracted
           ↓
6. Laboratory values are extracted
           ↓
7. Values are compared with reference ranges
           ↓
8. RAG retrieves relevant medical context
           ↓
9. Gemini generates an explanation
           ↓
10. FastAPI returns structured results
           ↓
11. Streamlit displays the analysis
```

---

## 🔐 Security & Privacy

- Uploaded reports are processed through temporary files.
- Temporary uploaded PDFs are removed after processing.
- API credentials are stored using environment variables.
- `.env` should not be committed to version control.
- Uploaded reports are not intended to be permanently stored by the API processing pipeline.

---

## ⚠️ Medical Disclaimer

This project is intended for educational and informational purposes.

The generated summaries are **not medical diagnoses** and should not replace professional medical advice.

Laboratory reference ranges can vary depending on the laboratory, testing method, patient characteristics, and clinical context.

Users should consult a qualified healthcare professional for interpretation of medical reports and treatment decisions.

---

## 🔮 Future Improvements

Possible future improvements include:

- Support for additional laboratory tests
- Improved OCR for scanned reports
- Better extraction from complex laboratory tables
- Automated reference-range extraction
- Authentication and user accounts
- Report history
- Database integration
- Expanded medical knowledge base
- Improved RAG evaluation
- Automated API testing
- Docker containerization
- Cloud deployment
- Structured downloadable PDF reports
- More advanced medical knowledge retrieval

---

## 👩‍💻 Author

**Antra Sharma**

B.Tech Computer Science & Engineering

GitHub:

https://github.com/antraa29

---

## 📌 Project Status

The project currently supports an end-to-end workflow from PDF upload to structured laboratory analysis and AI-generated explanation using:

- FastAPI
- Streamlit
- Google Gemini
- LangChain
- RAG
- FAISS
- Python

The project is actively being developed and can be extended with additional laboratory tests, medical knowledge sources, and deployment capabilities.

---

## ⚖️ Disclaimer

This application is a software project for educational and informational purposes. It does not provide professional medical diagnosis or treatment.
