import os
import json

import firebase_admin
import pandas as pd
from firebase_admin import credentials, firestore


def initialize_firebase():
    """Initialize the Firebase app using the service account key."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    service_account_path = os.path.join(project_root, "serviceAccountKey.json")
    firebase_credentials = credentials.Certificate(service_account_path)

    # Reuse the existing app if this script is run more than once in one process.
    if not firebase_admin._apps:
        firebase_admin.initialize_app(firebase_credentials)

    # Use the named Firestore database for this project.
    return firestore.client(database_id="bam-dan-production-db")


def fetch_collection_documents(database_client, collection_name):
    """Fetch all documents from a Firestore collection."""
    collection_reference = database_client.collection(collection_name)
    all_documents = []
    print(f"Starting Firestore fetch from '{collection_name}' collection")

    for document_snapshot in collection_reference.stream():
        document_data = document_snapshot.to_dict() or {}
        document_row = {
            "doc_id": document_snapshot.id,
        }

        if collection_name != "results":
            document_row.update(document_data)
            all_documents.append(document_row)
            continue

        # Copy flat fields and skip nested data structures until they are flattened.
        for field_name, field_value in document_data.items():
            if field_name in ("metadata", "rawAnswers"):
                continue
            document_row[field_name] = field_value

        # Flatten metadata fields with a "meta_" prefix.
        metadata_value = document_data.get("metadata") or {}
        for metadata_key, metadata_field_value in metadata_value.items():
            flattened_key = f"meta_{metadata_key}"
            document_row[flattened_key] = metadata_field_value

        # Flatten rawAnswers fields with a "q_" prefix.
        raw_answers_value = document_data.get("rawAnswers") or {}
        for answer_key, answer_value in raw_answers_value.items():
            flattened_key = f"q_{answer_key}"
            document_row[flattened_key] = answer_value

        all_documents.append(document_row)

        if len(all_documents) % 1000 == 0:
            print(f"Fetched {len(all_documents)} documents so far from '{collection_name}'")

    return all_documents


def save_results_to_parquet(all_documents):
    """Build a DataFrame from result documents and save it as a parquet file."""
    dataframe = pd.DataFrame(all_documents)
    print(f"{len(dataframe)} rows fetched")
    print("Columns:", list(dataframe.columns))
    dataframe.to_parquet("data/responses.parquet")
    print("Saved data/responses.parquet successfully")


def save_metadata_documents(metadata_documents):
    """Save metadata documents in raw and question-level formats."""
    with open("data/metadata.json", "w", encoding="utf-8") as metadata_file:
        json.dump(metadata_documents, metadata_file, ensure_ascii=False, indent=2)
    print("Saved data/metadata.json successfully")

    metadata_dataframe = pd.DataFrame(metadata_documents)
    metadata_dataframe.to_parquet("data/metadata.parquet")
    print("Saved data/metadata.parquet successfully")

    questions_document = next(
        (
            metadata_document
            for metadata_document in metadata_documents
            if metadata_document.get("doc_id") == "questions_v1"
        ),
        {},
    )
    questions_list = questions_document.get("questions") or []
    questions_dataframe = pd.DataFrame(questions_list)
    questions_dataframe.to_parquet("data/questions_v1.parquet")
    print("Saved data/questions_v1.parquet successfully")


def main():
    os.makedirs("data", exist_ok=True)
    print("Initializing Firebase")
    database_client = initialize_firebase()
    print("Firebase initialized successfully")
    result_documents = fetch_collection_documents(database_client, "results")
    save_results_to_parquet(result_documents)
    metadata_documents = fetch_collection_documents(database_client, "metadata")
    save_metadata_documents(metadata_documents)


if __name__ == "__main__":
    main()
