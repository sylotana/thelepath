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
    """Domain aggregate representing a processed document within the system.

    This entity encapsulates file information, its content
    segments (chunks), and associated metadata, serving as
    the primary unit for indexing and retrieval.
    """

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
        """Initialize a new Document with integrity checks.

        Args:
            file_path: Absolute or relative path to the source file.
            file_name: Human-readable name of the document.
            file_hash: Unique content signature for change detection.
            chunks: Optional pre-processed text segments.

        Raises:
            ValueError: If the provided file_path is empty or invalid.

        Returns:
            A validated Document entity.
        """
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
        """Partition the document content into overlapping semantic segments.

        This method implements the core RAG fragmentation logic, ensuring that
        large text bodies are indexed in searchable units while preserving
        context through configurable overlap.

        Args:
            chunk_size: Maximum number of characters per chunk.
            chunk_overlap: Number of characters to overlap between segments.
        """
        # Collect text from existing chunks (e.g.,
        # if a parser already populated them)
        # or assume we have one "raw" chunk containing the full text.
        full_text = "".join(c.content for c in self.chunks)

        if not full_text:
            return

        # Clear existing chunks to replace them with the new fragmentation
        self.chunks = []

        # Effective step size to prevent infinite loops and ensure progress
        step = max(1, chunk_size - chunk_overlap)
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
            start += step

    def vectorize(self, *, vectors: list[list[float]]) -> None:
        """Align vector embeddings with document chunks.

        This method updates the document's segments with their numerical
        representations, enabling downstream vector similarity searches.

        Args:
            vectors: A sequence of float lists, where each list represents
                an embedding for a chunk at the same index.

        Raises:
            ValueError: If the count of vectors does not align with the
                current number of chunks, ensuring data consistency.
        """
        if len(vectors) != len(self.chunks):
            raise ValueError(
                f"Vector alignment mismatch: received {len(vectors)},",
                f"expected {len(self.chunks)}.",
            )

        self.chunks = [
            c.copy_with_vector(vector=v) for c, v in zip(self.chunks, vectors)
        ]

    def ingest_text(
        self, *, content: str, metadata: dict[str, Any] | None = None
    ) -> None:
        """Ingest raw text into the document by creating an initial chunk.

        This method initializes the document's content state, merging
        provided metadata with file-specific information before
        creating the primary data segment.

        Args:
            content: The raw string content to be processed.
            metadata: Optional additional context (e.g., author, source, tags).
        """
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
        """Extract a flattened list of text content from all document segments.

        This property is primarily used by embedding services to perform
        batch vectorization without exposing the underlying Chunk entities.

        Returns:
            A list of raw strings representing the content of each chunk.
        """
        return [chunk.content for chunk in self.chunks]
