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
    """TODO: add correct docstring."""

    file_path: str
    file_name: str
    file_hash: str
    chunks: list[Chunk] = field(default_factory=list)
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
