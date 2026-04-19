from typing import Protocol

from .entities import Document


class VectorStorePort(Protocol):
    """TODO: add correct docstring."""

    def index_document(self, *, document: Document) -> None:
        """Save document and his vectors to base."""
        ...

    def needs_update(self, *, file_path: str, file_hash: str) -> bool:
        """Check, it is need to index file."""
        ...


class ParserPort(Protocol):
    """TODO: add correct docstring."""

    def parse_to_document(self, *, path: str, file_hash: str) -> Document:
        """TODO: add correct docstring."""
        ...


class FileSystemPort(Protocol):
    """TODO: add correct docstring."""

    def resolve_all_files(self, *, paths: list[str]) -> list[str]:
        """Get the simple file list."""
        ...

    def is_supported(self, *, path: str) -> bool:
        """TODO: add correct docstring."""
        ...

    def get_file_hash(self, *, path: str) -> str:
        """Get file hash for checking change."""
        ...


class EmbeddingsPort(Protocol):
    """Convert text data into numerical vector representations."""

    def get_embeddings(self, *, texts: list[str]) -> list[list[float]]:
        """Vectorize a list of strings into high-dimensional embeddings."""
        ...

    def get_query_embedding(self, *, text: str) -> list[float]:
        """Vectorize a single query string for search."""
        ...
