import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from rag.qa_chain import retrieve_context_for_patient_data

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.3,
)


def generate_summary(patient_data):
    # Retrieve grounding context for each lab value found in the report
    retrieved_context = retrieve_context_for_patient_data(patient_data)
    context_text = "\n\n".join(
        f"{test.replace('_', ' ').title()}: {text}"
        for test, text in retrieved_context.items()
    )

    prompt = ChatPromptTemplate.from_template("""
    You are a medical report assistant.

    Patient's report values:
    {patient_data}

    Reference information retrieved for these tests:
    {retrieved_context}

    Using the reference information above to ground your answer, provide:

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
            "patient_data": patient_data,
            "retrieved_context": context_text,
        }
    )

    content = response.content

    if isinstance(content, list):
        content = "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )

    return content