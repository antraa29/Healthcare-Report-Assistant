import re


def extract_patient_info(text):
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
        "tsh": r"TSH \(ULTRASENSITIVE\)\s+([\d\.]+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)

        if match:
            data[key] = match.group(1)

    return data