from ocr.pdf_parser import extract_text_from_pdf
from extraction.extractor import extract_patient_info
from llm.summarizer import generate_summary

pdf_path = "data/reports/blood_report.pdf"

text = extract_text_from_pdf(pdf_path)

patient_data = extract_patient_info(text)

print("Extracted Data:")
print(patient_data)

print("\nGenerating Summary...\n")

summary = generate_summary(patient_data)

print(summary)