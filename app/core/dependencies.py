import csv
from functools import lru_cache
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings
from app.schema.statistics import Statistic


# Paths
def get_data_folder() -> Path:
    if settings.DATA_DIR:
        return Path(settings.DATA_DIR)
    return Path(__file__).resolve().parents[2] / "data"


def get_data_path() -> Path:
    return get_data_folder() / "ecos_statistics.csv"


def get_index_path() -> Path:
    return get_data_folder() / "index.json"


@lru_cache
def get_embeddings() -> Embeddings:
    """Provides the embedding model instance."""
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY
    )


@lru_cache
def get_stats_data() -> List[Statistic]:
    """Loads and caches the raw statistics data."""
    data_path = get_data_path()
    if not data_path.exists():
        raise FileNotFoundError(f"Statistics file not found at {data_path}")

    with open(data_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [Statistic(**row) for row in reader]


@lru_cache
def get_vector_store() -> InMemoryVectorStore:
    """Loads or builds the In-Memory vector store."""
    index_path = get_index_path()
    embeddings_model = get_embeddings()

    if index_path.exists():
        try:
            return InMemoryVectorStore.load(str(index_path), embedding=embeddings_model)
        except Exception as e:
            print(f"Failed to load index: {e}. Rebuilding...")

    data = get_stats_data()
    documents = [
        Document(
            page_content=f"{stat.stat_name} {stat.stat_code}",
            metadata={"stat_code": stat.stat_code},
        )
        for stat in data
    ]

    store = InMemoryVectorStore.from_documents(documents, embeddings_model)
    store.dump(str(index_path))

    return store
