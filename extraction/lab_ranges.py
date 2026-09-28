LAB_RANGES = {
    "hba1c": {
        "unit": "%",
        "low": None,
        "high": 5.7,
        "reference": "< 5.7",
        "description": "HbA1c"
    },
    "fasting_blood_sugar": {
        "unit": "mg/dL",
        "low": 70,
        "high": 99,
        "reference": "70 - 99",
        "description": "Fasting Blood Sugar"
    },
    "uric_acid": {
        "unit": "mg/dL",
        "low": 3.5,
        "high": 7.2,
        "reference": "3.5 - 7.2",
        "description": "Uric Acid"
    },
    "vitamin_d": {
        "unit": "ng/mL",
        "low": 20,
        "high": None,
        "reference": ">= 20",
        "description": "Vitamin D"
    },
    "vitamin_b12": {
        "unit": "pg/mL",
        "low": 200,
        "high": 900,
        "reference": "200 - 900",
        "description": "Vitamin B12"
    },
    "prolactin": {
        "unit": "ng/mL",
        "low": 4,
        "high": 23,
        "reference": "4 - 23",
        "description": "Prolactin"
    },
    "tsh": {
        "unit": "mIU/L",
        "low": 0.4,
        "high": 4.0,
        "reference": "0.4 - 4.0",
        "description": "TSH"
    }
}


def classify_lab_value(test_name: str, value: float) -> str:
    """
    Classify a laboratory value using the configured
    reference thresholds.

    Returns:
        LOW, NORMAL, HIGH, or UNKNOWN
    """

    reference = LAB_RANGES.get(test_name)

    if not reference:
        return "UNKNOWN"

    low = reference["low"]
    high = reference["high"]

    if low is not None and value < low:
        return "LOW"

    if high is not None and value > high:
        return "HIGH"

    return "NORMAL"