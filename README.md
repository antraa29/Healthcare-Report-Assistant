# 🩺 Healthcare Report Assistant

An AI-powered healthcare report analysis application that extracts patient and laboratory information from PDF reports, evaluates laboratory values against configurable reference ranges, retrieves relevant medical context using RAG, and generates an easy-to-understand AI summary using Google Gemini.

## 🚀 Overview

Healthcare Report Assistant is an end-to-end AI application designed to simplify the interpretation of laboratory reports.

The system combines:

- PDF text extraction
- Pattern-based information extraction
- Deterministic laboratory classification
- Retrieval-Augmented Generation (RAG)
- FAISS vector search
- Google Gemini
- FastAPI
- Streamlit

### Workflow

```text
PDF Healthcare Report
        ↓
PDF Text Extraction
        ↓
Patient & Lab Data Extraction
        ↓
Lab Reference Range Classification
        ↓
RAG Context Retrieval
        ↓
Google Gemini
        ↓
AI-Generated Summary
        ↓
Streamlit Dashboard
