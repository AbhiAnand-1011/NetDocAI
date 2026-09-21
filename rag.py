from pathlib import Path

import chromadb
from google import genai
from google.genai import types

from config import settings


BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
CHROMA_DIR = BASE_DIR / "chroma_db"

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSIONS = 768


client = genai.Client(api_key=settings.gemini_api_key)

chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = chroma_client.get_or_create_collection(
    name="netdocai_knowledge",
    metadata={"hnsw:space": "cosine"},
)


def embed_text(text: str) -> list[float]:
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSIONS,
        ),
    )

    return result.embeddings[0].values


def chunk_text(text: str, chunk_size: int = 1000) -> list[str]:
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size]).strip()

        if chunk:
            chunks.append(chunk)

    return chunks


def build_index() -> int:
    documents = []
    ids = []
    embeddings = []
    metadatas = []

    for file_path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):
            documents.append(chunk)
            ids.append(f"{file_path.stem}-{index}")
            embeddings.append(embed_text(chunk))
            metadatas.append({"source": file_path.name})

    if not documents:
        return 0

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(documents)


def search_knowledge(query: str, n_results: int = 3) -> list[dict[str, str]]:
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    output = []

    for document, metadata in zip(documents, metadatas):
        output.append(
            {
                "source": metadata.get("source", "unknown"),
                "content": document,
            }
        )

    return output