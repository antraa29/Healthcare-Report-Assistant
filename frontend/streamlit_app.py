import pandas as pd
import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/api/reports/analyze"


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Healthcare Report Assistant",
    page_icon="🩺",
    layout="wide"
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.title("🩺 Healthcare AI")

    st.write(
        "Upload your blood report PDF for AI analysis."
    )

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


# -----------------------------
# Main Page
# -----------------------------

st.title("🩺 Healthcare Report Assistant")

st.caption(
    "AI-Powered Medical Report Analysis"
)

st.divider()


# -----------------------------
# Report Processing
# -----------------------------

if uploaded_file:

    st.success(
        "Report uploaded successfully."
    )

    with st.spinner("Analyzing report..."):

        try:

            response = requests.post(
                API_URL,
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                },
                timeout=120,
            )

            # -----------------------------
            # Successful Response
            # -----------------------------

            if response.status_code == 200:

                result = response.json()

                patient_data = result["patient_data"]
                lab_analysis = result["lab_analysis"]
                summary = result["summary"]

                st.success(
                    "Report analyzed successfully."
                )

            # -----------------------------
            # API Error
            # -----------------------------

            else:

                st.error(
                    f"API Error {response.status_code}: "
                    f"{response.text}"
                )

                st.stop()


        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the FastAPI backend. "
                "Make sure the API server is running."
            )

            st.stop()


        except requests.exceptions.Timeout:

            st.error(
                "The analysis took too long. "
                "Please try again."
            )

            st.stop()


        except Exception as e:

            st.error(
                f"An unexpected error occurred: {str(e)}"
            )

            st.stop()


    # -----------------------------
    # Patient Information
    # -----------------------------

    st.divider()

    st.subheader(
        "👤 Patient Information"
    )

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


    # -----------------------------
    # Blood Test Results
    # -----------------------------

    st.divider()

    st.subheader(
        "🧪 Blood Test Results"
    )

    rows = []

    for test_name, result_data in lab_analysis.items():

        status = result_data.get(
            "status",
            "UNKNOWN"
        )

        # Add visual indicator to status
        if status == "NORMAL":
            display_status = "🟢 NORMAL"

        elif status == "LOW":
            display_status = "🔴 LOW"

        elif status == "HIGH":
            display_status = "🔴 HIGH"

        else:
            display_status = "⚪ UNKNOWN"

        rows.append(
            {
                "Test": test_name.replace(
                    "_",
                    " "
                ).title(),

                "Result": result_data.get(
                    "value",
                    "N/A"
                ),

                "Unit": result_data.get(
                    "unit",
                    "N/A"
                ),

                "Reference Range": result_data.get(
                    "reference",
                    "N/A"
                ),

                "Status": display_status,
            }
        )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # -----------------------------
    # Result Overview
    # -----------------------------

    st.divider()

    st.subheader(
        "📊 Result Overview"
    )

    normal_count = sum(
        1
        for item in lab_analysis.values()
        if item.get("status") == "NORMAL"
    )

    low_count = sum(
        1
        for item in lab_analysis.values()
        if item.get("status") == "LOW"
    )

    high_count = sum(
        1
        for item in lab_analysis.values()
        if item.get("status") == "HIGH"
    )

    unknown_count = sum(
        1
        for item in lab_analysis.values()
        if item.get("status") == "UNKNOWN"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Normal",
            normal_count
        )

    with col2:

        st.metric(
            "Low",
            low_count
        )

    with col3:

        st.metric(
            "High",
            high_count
        )

    with col4:

        st.metric(
            "Unknown",
            unknown_count
        )


    # -----------------------------
    # AI Medical Summary
    # -----------------------------

    st.divider()

    st.subheader(
        "🤖 AI Medical Summary"
    )

    with st.container(
        border=True
    ):

        st.write(summary)


    # -----------------------------
    # Download Summary
    # -----------------------------

    st.divider()

    st.download_button(
        label="📥 Download Summary",
        data=summary,
        file_name="medical_summary.txt",
        mime="text/plain",
        use_container_width=True
    )


# -----------------------------
# Medical Disclaimer
# -----------------------------

st.divider()

st.caption(
    "This AI-generated summary is for informational purposes only "
    "and should not replace professional medical advice."
)