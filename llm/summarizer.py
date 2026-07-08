import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
)


def generate_summary(patient_data):

    prompt = ChatPromptTemplate.from_template("""
    You are a medical report assistant.

    Analyze the following report values:

    {patient_data}

    Provide:

    1. Overall summary.
    2. Normal values.
    3. Abnormal values.
    4. Possible health concerns.
    5. Lifestyle recommendations.

    Explain everything in simple language.
    Do not provide a medical diagnosis.
    """)

    chain = prompt | llm

    response = chain.invoke(
        {
            "patient_data": patient_data
        }
    )

    return response.content