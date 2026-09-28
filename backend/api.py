import os
import shutil
import tempfile
import traceback

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from ocr.pdf_parser import extract_text_from_pdf
from extraction.extractor import (
    extract_patient_info,
    analyze_lab_results,
)
from llm.summarizer import generate_summary


# -----------------------------
# API Response Model
# -----------------------------

class ReportAnalysisResponse(BaseModel):
    success: bool
    patient_data: dict
    lab_analysis: dict
    summary: str


# -----------------------------
# FastAPI Application
# -----------------------------

app = FastAPI(
    title="Healthcare Report Assistant API",
    description="AI-powered healthcare report analysis API",
    version="1.0.0",
)


# -----------------------------
# Healthcare Report Pipeline
# -----------------------------

def process_report(pdf_path):
    """
    Complete healthcare report processing pipeline:

    PDF
      ↓
    Text Extraction
      ↓
    Patient/Lab Data Extraction
      ↓
    Deterministic Lab Classification
      ↓
    RAG + Gemini AI Summary
    """

    # Step 1: Extract text from PDF
    print("\n[1/4] Extracting text from PDF...")

    text = extract_text_from_pdf(pdf_path)

    if not text or not text.strip():
        raise ValueError(
            "No readable text was found in the PDF."
        )

    print("[OK] PDF text extracted.")

    # Step 2: Extract patient and laboratory information
    print("\n[2/4] Extracting patient information...")

    patient_data = extract_patient_info(text)

    if not patient_data:
        raise ValueError(
            "No patient or laboratory information could be extracted."
        )

    print("[OK] Patient data extracted:")
    print(patient_data)

    # Step 3: Classify laboratory values
    print("\n[3/4] Classifying laboratory results...")

    lab_analysis = analyze_lab_results(patient_data)

    print("[OK] Lab analysis:")
    print(lab_analysis)

    # Step 4: Generate AI summary
    print("\n[4/4] Generating AI summary...")

    summary = generate_summary(patient_data)

    if not summary:
        raise ValueError(
            "AI summary generation returned an empty response."
        )

    print("[OK] AI summary generated.")

    return (
        patient_data,
        lab_analysis,
        summary,
    )


# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
def root():
    """Health check endpoint."""

    return {
        "message": "Healthcare Report Assistant API is running",
        "version": "1.0.0",
    }


# -----------------------------
# Health Check Endpoint
# -----------------------------

@app.get("/api/health")
def health_check():
    """API health check."""

    return {
        "status": "healthy"
    }


# -----------------------------
# Report Analysis Endpoint
# -----------------------------

@app.post(
    "/api/reports/analyze",
    response_model=ReportAnalysisResponse,
)
async def analyze_report(
    file: UploadFile = File(...)
):
    """
    Upload a healthcare report PDF and receive:

    - Extracted patient information
    - Laboratory values
    - Deterministic LOW/NORMAL/HIGH classification
    - AI-generated medical summary
    """

    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    temp_path = None

    try:

        # -----------------------------
        # Create temporary PDF
        # -----------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as temp_file:

            shutil.copyfileobj(
                file.file,
                temp_file
            )

            temp_path = temp_file.name

        print("\n========================================")
        print("NEW REPORT ANALYSIS")
        print("========================================")

        print(f"Temporary PDF: {temp_path}")

        # -----------------------------
        # Process report
        # -----------------------------

        (
            patient_data,
            lab_analysis,
            summary,
        ) = process_report(temp_path)

        print("\n========================================")
        print("REPORT ANALYSIS COMPLETE")
        print("========================================\n")

        return {
            "success": True,
            "patient_data": patient_data,
            "lab_analysis": lab_analysis,
            "summary": summary,
        }

    except ValueError as exc:

        print("\n[VALUE ERROR]")
        print(str(exc))

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        # IMPORTANT:
        # Print the real error in the terminal.
        print("\n========================================")
        print("ERROR WHILE PROCESSING REPORT")
        print("========================================")

        print(f"\nError type: {type(exc).__name__}")
        print(f"Error message: {str(exc)}")

        print("\nFull traceback:")
        traceback.print_exc()

        print("========================================\n")

        raise HTTPException(
            status_code=500,
            detail=(
                f"Report processing failed: "
                f"{type(exc).__name__}: {str(exc)}"
            ),
        )

    finally:

        # -----------------------------
        # Delete temporary PDF
        # -----------------------------

        if temp_path and os.path.exists(temp_path):

            try:
                os.remove(temp_path)
                print("[OK] Temporary PDF deleted.")
            except Exception as cleanup_error:
                print(
                    f"[WARNING] Could not delete temporary file: "
                    f"{cleanup_error}"
                )