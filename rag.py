import os
import sys
from pathlib import Path

import chromadb
from google import genai
from google.genai import types

from config import settings


BASE_DIR = Path(__file__).resolve().parent

SOURCE_KNOWLEDGE_DIR = BASE_DIR / "knowledge"
INSTALLED_KNOWLEDGE_DIR = (
    Path(sys.prefix) / "share" / "netdocai" / "knowledge"
)

KNOWLEDGE_DIR = (
    SOURCE_KNOWLEDGE_DIR
    if SOURCE_KNOWLEDGE_DIR.is_dir()
    else INSTALLED_KNOWLEDGE_DIR
)

DATA_DIR = (
    Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
    .expanduser()
    / "netdocai"
)

CHROMA_DIR = DATA_DIR / "chroma_db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSIONS = 768

chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = chroma_client.get_or_create_collection(
    name="netdocai_knowledge",
    metadata={"hnsw:space": "cosine"},
)


def embed_text(text: str) -> list[float]:
    with genai.Client(api_key=settings.gemini_api_key) as client:
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
    if not KNOWLEDGE_DIR.is_dir():
        raise FileNotFoundError(
            f"Knowledge directory not found: {KNOWLEDGE_DIR}"
        )

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
        raise RuntimeError(
            "No knowledge documents found for indexing."
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(documents)


def ensure_index() -> None:
    if collection.count() > 0:
        return

    print("[RAG] Initializing knowledge base...")

    count = build_index()

    print(f"[RAG] Indexed {count} knowledge chunks.")


def search_knowledge(
    query: str,
    n_results: int = 3,
) -> list[dict[str, str]]:
    ensure_index()

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count()),
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