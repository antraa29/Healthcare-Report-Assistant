import os
import sys
import pandas as pd
import streamlit as st

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from backend.api import process_report

st.set_page_config(
    page_title="Healthcare Report Assistant",
    page_icon="🩺",
    layout="wide"
)

with st.sidebar:

    st.title("🩺 Healthcare AI")

    st.write("Upload your blood report PDF for AI analysis.")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    st.divider()

    st.subheader("Supported Reports")

    st.write("✅ Blood Test Reports")
    st.write("✅ Health Checkup Reports")
    st.write("✅ Diagnostic Reports")

    st.divider()

    st.caption(
        "Powered by Gemini AI"
    )

st.title("🩺 Healthcare Report Assistant")

st.caption(
    "AI-Powered Medical Report Analysis"
)

st.divider()

if uploaded_file:

    os.makedirs("data/reports", exist_ok=True)

    save_path = os.path.join(
        "data",
        "reports",
        uploaded_file.name
    )

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Report uploaded successfully.")

    with st.spinner("Analyzing report..."):

        patient_data, summary = process_report(save_path)

    st.divider()

    st.subheader("👤 Patient Information")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Patient Name",
            patient_data.get(
                "patient_name",
                "Not Found"
            )
        )

    with col2:

        st.metric(
            "Age / Gender",
            patient_data.get(
                "age_gender",
                "Not Found"
            )
        )

    st.divider()

    st.subheader("🧪 Blood Test Results")

    rows = []

    for key, value in patient_data.items():

        if key not in ["patient_name", "age_gender"]:

            rows.append(
                {
                    "Test": key.replace("_", " ").title(),
                    "Value": value
                }
            )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🤖 AI Medical Summary")

    with st.container(border=True):

        st.write(summary)

    st.divider()

    st.download_button(
        label="📥 Download Summary",
        data=summary,
        file_name="medical_summary.txt",
        mime="text/plain",
        use_container_width=True
    )

st.divider()

st.caption(
    "This AI-generated summary is for informational purposes only and should not replace professional medical advice."
)