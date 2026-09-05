from rag.vector_store import load_vector_store

_vector_store = None


def _get_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = load_vector_store()
    return _vector_store


def retrieve_context_for_test(test_name: str, k: int = 1) -> str:
    """Given a lab test name (e.g. 'hba1c', 'vitamin_d'), retrieves the
    most relevant explanation chunk from the knowledge base."""
    store = _get_store()
    query = test_name.replace("_", " ")
    results = store.similarity_search(query, k=k)
    return "\n".join(doc.page_content for doc in results)


def retrieve_context_for_patient_data(patient_data: dict) -> dict:
    """Runs retrieval for every lab value found in the extracted patient data
    (skipping non-lab fields like name/age), returning {test_name: retrieved_text}."""
    skip_fields = {"patient_name", "age_gender"}
    context = {}

    for test_name in patient_data:
        if test_name in skip_fields:
            continue
        context[test_name] = retrieve_context_for_test(test_name)

    return context