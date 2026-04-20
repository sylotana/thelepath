import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)  # Make immutable for reliability
class Chunk:
    """Fundamental unit of text with its embedding and metadata.

    This class serves as a Value Object in the domain, ensuring that processed
    text units maintain their integrity and identity across the pipeline.
    """

    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    vector: list[float] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def create(
        cls,
        *,
        content: str,
        metadata: dict[str, Any] | None = None,
        id: str | None = None,
    ) -> "Chunk":
        """Create a Chunk with automatic ID and metadata handling.

        Args:
            content: The raw text string to be stored.
            metadata: Optional dictionary with source info, tags, etc.
            id: Unique identifier. If None, a UUID is generated.

        Returns:
            A new immutable Chunk instance.
        """
        return cls(
            content=content,
            metadata=metadata or {},
            id=id or str(uuid.uuid4()),
        )

    def copy_with_vector(self, *, vector: list[float]) -> "Chunk":
        """Creates a new Chunk instance with an updated vector embedding.

        Since the class is frozen (immutable), this method implements
        the evolution of a Chunk when its vector representation is computed.

        Args:
            vector: A list of floats representing the text embedding.

        Returns:
            A new Chunk instance with the same identity
            but updated vector data.
        """
        return Chunk(
            content=self.content,
            metadata=self.metadata,
            vector=vector,
            id=self.id,
        )


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
        self,
        *,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
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
            new_chunk = Chunk.create(
                content=chunk_content,
                metadata={
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

    def vectorize(self, *, vectors: list[list[float]]) -> None:
        """TODO: add correct docstring."""
        if len(vectors) != len(self.chunks):
            raise ValueError(
                "The number of vectors does not match the number of fragments."
            )

        self.chunks = [
            c.copy_with_vector(vector=v) for c, v in zip(self.chunks, vectors)
        ]

    def ingest_text(
        self, *, content: str, metadata: dict[str, Any] | None = None
    ) -> None:
        """TODO: add correct docstring."""
        initial_metadata = {"file_path": self.file_path}
        if metadata:
            initial_metadata.update(metadata)

        # Create one start chunk
        self.chunks = [
            Chunk.create(
                content=content,
                metadata=initial_metadata,
            )
        ]

    @property
    def text_batches(self) -> list[str]:
        """Returns a list of texts of all fragments for vectorization."""
        return [chunk.content for chunk in self.chunks]
