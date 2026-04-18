# backend/src/infrastructure/adapters/parser.py
from src.domain.entities import Chunk, Document
from src.domain.ports import ParserPort


class SimpleParserAdapter(ParserPort):
    """Basic parser that reads file content and wraps it into a Document."""

    def parse_to_document(self, *, path: str, file_hash: str) -> Document:
        """Reads raw text and creates a basic Document entity."""
        print(f"[Parser] Parsing file: {path}")

        with open(path, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Create a single chunk for now
        # Later we will add chunking logic (recursive character splitter, etc.)
        chunk = Chunk(content=content, metadata={"source": path})

        return Document.create(
            file_path=path,
            file_name=path.split("/")[-1],  # Simple way to get filename
            file_hash=file_hash,
            chunks=[chunk],
        )
