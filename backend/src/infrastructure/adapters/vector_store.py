# backend/src/infrastructure/adapters/vector_store.py
from src.domain.entities import Document
from src.domain.ports import VectorStorePort


class InMemoryVectorStoreAdapter(VectorStorePort):
    """A simple in-memory implementation for development and testing."""

    def __init__(self) -> None:
        """TODO: add correct docstring."""
        # Using a dict to simulate storage: {file_path: file_hash}
        self._indexed_files: dict[str, str] = {}

    def needs_update(self, *, file_path: str, file_hash: str) -> bool:
        """Check if the file is missing or the hash has changed."""
        existing_hash = self._indexed_files.get(file_path)
        return existing_hash != file_hash

    def index_document(self, *, document: Document) -> None:
        """Simulate saving the document to a vector database."""
        print(f"[VectorStore] Indexing document: {document.file_name}")
        print(f"[VectorStore] Saving {len(document.chunks)} chunks...")
        self._indexed_files[document.file_path] = document.file_hash
