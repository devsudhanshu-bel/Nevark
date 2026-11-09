# RAG Engine

## 1. Overview

The `rag_engine.py` module implements vector-based memory storage and semantic retrieval for Nevark AI using ChromaDB.

It converts text into numerical embeddings using the existing `create_embedding()` function from `app/core/embeddings.py` and stores those embeddings alongside their original text in a persistent ChromaDB collection.

The module exposes two primary functions:

- `save_memory_to_vector_db()` – Converts text into an embedding and stores it in ChromaDB.
- `retrieve_relevant_memories()` – Converts a search query into an embedding and retrieves the most relevant stored documents.

This provides a foundation for semantic memory retrieval, where information can be retrieved based on meaning rather than requiring an exact keyword match.

## 2. Dependencies

```python
import chromadb

from app.core.embeddings import (
    create_embedding
)
```

| Dependency | Purpose |
|---|---|
| `chromadb` | Provides persistent vector database storage and similarity-based retrieval |
| `create_embedding()` | Converts text and queries into numerical vector representations |

The embedding-generation functionality is reused from `app/core/embeddings.py`, keeping text encoding separate from vector storage and retrieval.

## 3. ChromaDB Client Initialization

```python
client = chromadb.PersistentClient(
    path="vector_store/chroma_db"
)
```

The module initializes a persistent ChromaDB client.

The database is stored locally at:

`vector_store/chroma_db`

Using `PersistentClient` allows the vector database to persist its data on disk rather than existing only in application memory.

This means stored vectors and documents can remain available across application restarts, provided the same storage location is used.

## 4. Collection Initialization

```python
collection = client.get_or_create_collection(
    name="nevark_memory"
)
```

The module retrieves an existing collection named `nevark_memory` or creates it if it does not already exist.

A ChromaDB collection acts as a logical container for stored documents and their associated embeddings.

| Property | Value |
|---|---|
| Database | ChromaDB |
| Storage path | `vector_store/chroma_db` |
| Collection name | `nevark_memory` |
| Stored content | Text documents and embeddings |

The collection is initialized at module level and reused by both memory-storage and retrieval functions.

## 5. Core Function: `save_memory_to_vector_db()`

```python
def save_memory_to_vector_db(
    text: str
):
```

This function stores a text document in the ChromaDB vector collection.

It accepts a string, generates its embedding, and adds both the original text and its vector representation to the collection.

### Input parameter

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Text that needs to be stored in the vector database |

### Step 1: Generate the embedding

```python
embedding = create_embedding(
    text
)
```

The input text is passed to `create_embedding()` from `app/core/embeddings.py`.

That function uses the `all-MiniLM-L6-v2` Sentence Transformer model to convert the text into a numerical vector.

The generated embedding represents the semantic information contained in the input text.

### Step 2: Add the document to ChromaDB

```python
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
```

The `collection.add()` method stores the document and its embedding.

Three fields are supplied:

| Field | Value | Purpose |
|---|---|---|
| `ids` | Generated string ID | Uniquely identifies the stored record |
| `embeddings` | Generated embedding | Stores the numerical representation |
| `documents` | Original text | Stores the original content |

### Document ID generation

```python
str(collection.count() + 1)
```

The current number of records in the collection is retrieved using `collection.count()`.

One is added to that number, and the result is converted into a string.

For example:

- If the collection contains 0 records, the generated ID is `"1"`.
- If it contains 5 records, the generated ID is `"6"`.
- If it contains 10 records, the generated ID is `"11"`.

This provides a simple sequential ID-generation mechanism.

**Implementation consideration:** This approach assumes that the collection's record count can safely be used to generate the next unique ID. If records are deleted, IDs may be reused. ChromaDB can reject an `add()` operation when the generated ID already exists. Concurrent insertions can also produce ID collisions.

## 6. Core Function: `retrieve_relevant_memories()`

```python
def retrieve_relevant_memories(
    query: str,
    top_k: int = 5
):
```

This function performs semantic retrieval against the stored ChromaDB collection.

Instead of searching for exact words, it converts the query into an embedding and uses ChromaDB's vector-query functionality to retrieve relevant stored documents.

### Input parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | Required | Text used to search the vector database |
| `top_k` | `int` | `5` | Maximum number of documents requested |

### Step 1: Check whether the collection contains data

```python
if collection.count() == 0:
    return []
```

Before performing a vector search, the function checks whether the collection contains any records.

If the collection is empty, it returns an empty list immediately.

This avoids performing a query against an empty collection.

### Step 2: Generate the query embedding

```python
embedding = create_embedding(
    query
)
```

The input query is converted into a numerical embedding using the same `create_embedding()` function used during storage.

Using the same embedding model for stored documents and incoming queries ensures that their vectors are generated within the same embedding space.

This allows ChromaDB to compare the query vector with the stored document vectors.

### Step 3: Perform vector similarity retrieval

```python
results = collection.query(
    query_embeddings=[
        embedding
    ],

    n_results=min(
        top_k,
        collection.count()
    )
)
```

The function submits the generated query embedding to ChromaDB.

Two important parameters are supplied:

**`query_embeddings`**

Contains the numerical embedding generated from the user's query.

**`n_results`**

Controls the maximum number of results requested.

The expression:

```python
min(
    top_k,
    collection.count()
)
```

ensures that the requested result count does not exceed the number of documents currently stored.

For example:

| Collection count | `top_k` | Requested results |
|---:|---:|---:|
| 3 | 5 | 3 |
| 10 | 5 | 5 |
| 20 | 10 | 10 |

ChromaDB performs vector-based retrieval and returns the matching records.

### Step 4: Extract retrieved documents

```python
documents = results.get(
    "documents",
    []
)
```

The function extracts the `documents` field from the ChromaDB query response.

If the field is unavailable, it defaults to an empty list.

The returned documents are organized by query, so the first element represents the document results for the single query submitted by this function.

### Step 5: Handle empty results

```python
if not documents:
    return []
```

If the documents field is empty or unavailable, the function returns an empty list.

### Step 6: Return the retrieved memories

```python
return documents[0]
```

The function returns the first query's list of retrieved documents.

The result is a list of original text strings, not embeddings or complete ChromaDB result objects.

## 7. Complete Execution Flow

### Memory storage flow

1. A backend component supplies text to `save_memory_to_vector_db()`.
2. The text is passed to `create_embedding()`.
3. Sentence Transformers generates a numerical embedding.
4. ChromaDB generates a record ID using the current collection count.
5. The ID, embedding, and original text are stored in `nevark_memory`.
6. The persistent database retains the stored information on disk.

### Memory retrieval flow

1. A backend component supplies a search query.
2. The function checks whether the collection contains records.
3. The query is converted into an embedding.
4. ChromaDB compares the query embedding against stored vectors.
5. The requested number of relevant documents is retrieved.
6. The original document strings are extracted.
7. The retrieved text documents are returned to the caller.

## 8. Relationship with the Embeddings Module

This module depends directly on:

`app/core/embeddings.py`

The embeddings module is responsible for converting text into vectors, while the RAG engine is responsible for storing and retrieving those vectors.

| Component | Responsibility |
|---|---|
| `embeddings.py` | Generates text embeddings |
| `rag_engine.py` | Stores embeddings and documents in ChromaDB |
| ChromaDB | Persists vector records and performs vector queries |

This separation allows the embedding-generation logic to be reused without duplicating model initialization or encoding functionality.

## 9. Relationship with the Conversation Memory Engine

Nevark currently has two distinct memory mechanisms.

| Feature | `memory_engine.py` | `rag_engine.py` |
|---|---|---|
| Storage mechanism | JSON file | ChromaDB |
| Storage location | `memory/conversations.json` | `vector_store/chroma_db` |
| Stored information | User-assistant exchanges | Text documents |
| Retrieval approach | Recent entries using list slicing | Embedding-based vector retrieval |
| Main purpose | Conversation history | Semantic memory retrieval |
| Output | Role-based message dictionaries | List of retrieved text documents |

The two modules serve different purposes.

The JSON memory engine retrieves recent conversational context, while the RAG engine retrieves stored text based on vector similarity.

**Important:** The supplied `rag_engine.py` does not automatically synchronize with `memory_engine.py`. It also does not automatically save every conversation exchange into ChromaDB. A calling component must explicitly invoke the relevant functions.

## 10. Current Implementation Scope

The module currently provides:

- Persistent ChromaDB client initialization.
- Automatic collection creation or retrieval.
- Integration with the Sentence Transformer embedding module.
- Text-to-vector storage.
- Original document storage.
- Basic sequential record ID generation.
- Vector-based query retrieval.
- Configurable retrieval count through `top_k`.
- Empty-collection handling.
- Empty-document-result handling.

The module does not currently implement:

- Automatic conversation-to-vector synchronization.
- User-specific or session-specific filtering.
- Document metadata storage.
- Document chunking.
- Explicit similarity thresholds.
- Custom distance metrics in the supplied code.
- Retrieval-result reranking.
- Memory expiration or deletion.
- Automatic LLM context construction.
- Direct LLM response generation.

## 11. Important Implementation Considerations

### 11.1 Document granularity

The function stores the entire supplied text as one document.

There is no chunking or splitting logic in this module. If large text is supplied, it is stored as a single document rather than multiple smaller records.

### 11.2 Retrieval limit

The default `top_k` is 5, but callers can supply another value.

The function caps the requested number of results at the collection count.

### 11.3 Returned data

The function returns only the retrieved document strings.

It does not return:

- Document IDs.
- Similarity distances.
- Metadata.
- Embedding vectors.

### 11.4 Empty collection behavior

The function checks the collection count before generating a query embedding.

This avoids unnecessary embedding generation when no documents are available.

### 11.5 Persistent storage

The ChromaDB client uses a local persistent directory. Its availability depends on the application using the same configured storage path.

## 12. Summary

The `rag_engine.py` module provides the vector-based memory storage and semantic retrieval functionality for Nevark AI.

It integrates the Sentence Transformer embedding model with ChromaDB to convert text into numerical vectors, store original documents, and retrieve relevant content using vector queries.

Together with `memory_engine.py`, it provides a separate retrieval mechanism alongside conventional conversation-history storage.

At its current stage, the module establishes the core vector-storage and retrieval layer, while higher-level components remain responsible for deciding what information to store and how retrieved documents should be used in an AI response.