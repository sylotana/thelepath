import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)  # Make immutable for reliability
class Chunk:
    """TODO: add correct docstring."""

    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    vector: list[float] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Document:
    """Domain entity representing a processed file."""

    file_path: str
    file_name: str
    file_hash: str
    chunks: list[Chunk] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def create(
        cls,
        *,
        file_path: str,
        file_name: str,
        file_hash: str,
        chunks: list[Chunk] | None = None,
    ) -> "Document":
        """TODO: add correct docstring."""
        # In the future, this will use Result.ok(...) or Result.fail(...)
        # For now — basic validation
        if not file_path:
            raise ValueError("File path cannot be empty")

        return cls(
            file_path=file_path,
            file_name=file_name,
            file_hash=file_hash,
            chunks=chunks or [],
        )

    def split_into_chunks(
        self, *, chunk_size: int, chunk_overlap: int
    ) -> None:
        """Split the document's content into smaller semantic chunks.

        This is a core business rule for RAG: determining how data
        is fragmented for vector search.
        """
        # Collect text from existing chunks (e.g.,
        # if a parser already populated them)
        # or assume we have one "raw" chunk containing the full text.
        full_text = "".join(c.content for c in self.chunks)

        if not full_text:
            return

        # Clear existing chunks to replace them with the new fragmentation
        self.chunks = []

        start = 0
        text_len = len(full_text)

        while start < text_len:
            end = start + chunk_size
            chunk_content = full_text[start:end]

            # Create a domain Chunk object.
            # UUID is generated automatically inside the Chunk class.
            new_chunk = Chunk(
                content=chunk_content,
                metadata={
                    "file_path": self.file_path,
                    "start_index": start,
                    "end_index": min(end, text_len),
                    **self.metadata,  # Spread general document metadata
                },
            )
            self.chunks.append(new_chunk)

            # Shift the window using chunk_overlap
            start += chunk_size - chunk_overlap

            # Guard against infinite loops if overlap >= chunk_size
            if chunk_size <= chunk_overlap:
                break
