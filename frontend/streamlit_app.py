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

            # Send PDF directly to FastAPI
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


        # -----------------------------
        # Connection Error
        # -----------------------------

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the FastAPI backend. "
                "Make sure the API server is running."
            )

            st.stop()


        # -----------------------------
        # Timeout Error
        # -----------------------------

        except requests.exceptions.Timeout:

            st.error(
                "The analysis took too long. "
                "Please try again."
            )

            st.stop()


        # -----------------------------
        # Unexpected Error
        # -----------------------------

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

    for key, value in patient_data.items():

        if key not in [
            "patient_name",
            "age_gender"
        ]:

            rows.append(
                {
                    "Test": key.replace(
                        "_",
                        " "
                    ).title(),

                    "Value": value
                }
            )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
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