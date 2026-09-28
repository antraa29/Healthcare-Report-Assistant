import os
import shutil
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from ocr.pdf_parser import extract_text_from_pdf
from extraction.extractor import extract_patient_info
from llm.summarizer import generate_summary

class ReportAnalysisResponse(BaseModel):
    success: bool
    patient_data: dict
    summary: str


app = FastAPI(
    title="Healthcare Report Assistant API",
    description="AI-powered healthcare report analysis API",
    version="1.0.0",
)


def process_report(pdf_path):
    """
    Complete healthcare report processing pipeline:

    PDF → Text Extraction → Patient/Lab Data Extraction → AI Summary
    """

    # Step 1: Extract text from PDF
    text = extract_text_from_pdf(pdf_path)

    if not text or not text.strip():
        raise ValueError("No readable text was found in the PDF.")

    # Step 2: Extract patient and laboratory information
    patient_data = extract_patient_info(text)

    # Step 3: Generate AI summary
    summary = generate_summary(patient_data)

    return patient_data, summary


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "message": "Healthcare Report Assistant API is running",
        "version": "1.0.0",
    }


@app.get("/api/health")
def health_check():
    """API health check."""
    return {
        "status": "healthy"
    }


@app.post(
    "/api/reports/analyze",
    response_model=ReportAnalysisResponse,
)
async def analyze_report(file: UploadFile = File(...)):
    """
    Upload a healthcare report PDF and receive
    extracted laboratory information and an AI-generated summary.
    """

    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    temp_path = None

    try:
        # Create a temporary file so uploaded reports
        # are not permanently stored on the server.
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as temp_file:

            shutil.copyfileobj(file.file, temp_file)

            temp_path = temp_file.name

        # Process the uploaded report
        patient_data, summary = process_report(temp_path)

        return {
            "success": True,
            "patient_data": patient_data,
            "summary": summary,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the report.",
        )

    finally:
        # Always remove the temporary uploaded PDF.
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)