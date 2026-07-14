from ocr.pdf_parser import extract_text_from_pdf
from extraction.extractor import extract_patient_info
from llm.summarizer import generate_summary


def process_report(pdf_path):
    """
    Complete backend pipeline:
    PDF → Text → Extract Data → AI Summary
    """

    # Step 1: Extract text from PDF
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Extract important values
    patient_data = extract_patient_info(text)

    # Step 3: Generate AI summary
    summary = generate_summary(patient_data)

    return patient_data, summary