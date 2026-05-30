import chromadb

from app.core.embeddings import (
    create_embedding
)

client = chromadb.PersistentClient(
    path="vector_store/chroma_db"
)

collection = client.get_or_create_collection(
    name="nevark_memory"
)


def save_memory_to_vector_db(
    text: str
):

    embedding = create_embedding(
        text
    )

    collection.add(

        ids=[
            str(
                collection.count() + 1
            )
        ],

        embeddings=[
            embedding
        ],

        documents=[
            text
        ]
    )


def retrieve_relevant_memories(
    query: str,
    top_k: int = 5
):

    if collection.count() == 0:

        return []

    embedding = create_embedding(
        query
    )

    results = collection.query(

        query_embeddings=[
            embedding
        ],

        n_results=min(
            top_k,
            collection.count()
        )
    )

    documents = results.get(
        "documents",
        []
    )

    if not documents:

        return []

    return documents[0]