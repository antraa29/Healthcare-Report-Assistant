import re

from extraction.lab_ranges import (
    LAB_RANGES,
    classify_lab_value,
)


def extract_patient_info(text):
    """
    Extract patient information and laboratory values
    from the report text.
    """

    data = {}

    patterns = {
        "patient_name": r"PATIENT NAME\s*:\s*(.*)",
        "age_gender": r"AGE/SEX\s*:\s*(.*)",
        "hba1c": r"HBA1C\s+([\d\.]+)",
        "fasting_blood_sugar": r"FBS-FASTING BLOOD SUGAR\(GLUCOSE\)\s+([\d\.]+)",
        "uric_acid": r"URIC ACID\s+([\d\.]+)",
        "vitamin_d": r"25 - HYDROXYVITAMIN D\s+([\d\.]+)",
        "vitamin_b12": r"VITAMIN B12\s+([\d\.]+)",
        "prolactin": r"PROLACTIN\s+([\d\.]+)",
        "tsh": r"TSH \(ULTRASENSITIVE\)\s+([\d\.]+)",
    }

    for key, pattern in patterns.items():

        match = re.search(pattern, text)

        if match:
            value = match.group(1)

            # Keep patient information as text
            if key not in ["patient_name", "age_gender"]:
                value = float(value)

            data[key] = value

    return data


def analyze_lab_results(patient_data):
    """
    Classify extracted laboratory values as LOW, NORMAL,
    HIGH, or UNKNOWN using configured reference ranges.

    Also returns the unit and reference range for each test.
    """

    analysis = {}

    for test_name, value in patient_data.items():

        # Skip non-laboratory fields
        if test_name in ["patient_name", "age_gender"]:
            continue

        try:

            numeric_value = float(value)

            # Determine LOW / NORMAL / HIGH
            status = classify_lab_value(
                test_name,
                numeric_value
            )

            # Get metadata for the laboratory test
            reference = LAB_RANGES.get(
                test_name,
                {}
            )

            analysis[test_name] = {
                "value": numeric_value,
                "unit": reference.get(
                    "unit",
                    ""
                ),
                "reference": reference.get(
                    "reference",
                    ""
                ),
                "status": status,
            }

        except (ValueError, TypeError):

            analysis[test_name] = {
                "value": value,
                "unit": "",
                "reference": "",
                "status": "UNKNOWN",
            }

    return analysis