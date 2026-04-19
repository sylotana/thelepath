from qdrant_client import QdrantClient, models

from src.domain.entities import Document


class QdrantVectorStoreAdapter:
    """TODO: add correct docstring."""

    def __init__(
        self,
        *,
        path: str = "./qdrant_data:",
        collection_name: str = "documents",
    ) -> None:
        """TODO: add correct docstring."""
        self.client = QdrantClient(path=path)
        self.collection_name = collection_name
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """Create collection, if it's not exist."""
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # Dimension bge-small-en-v1.5
                    distance=models.Distance.COSINE,
                ),
            )

    def needs_update(self, *, file_path: str, file_hash: str) -> bool:
        """Find document in base of file_path and check hash."""
        results, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="file_path",
                        match=models.MatchValue(value=file_path),
                    )
                ]
            ),
            limit=1,
            with_payload=True,
        )

        print(f"[Debug] Search for {file_path}: found {len(results)} points")

        if not results:
            return True

        # Give payload and check so is exist
        payload = results[0].payload
        if payload is None:
            return True  # If not data, think so it's update

        db_hash = payload.get("file_hash")
        print(f"[Debug] DB Hash: '{db_hash}' (type: {type(db_hash)})")
        print(f"[Debug] Local Hash: '{file_hash}' (type: {type(file_hash)})")

        has_changed = db_hash != file_hash
        print(f"[Debug] Comparison (changed?): {has_changed}")

        return has_changed

    def index_document(self, *, document: Document) -> None:
        """Make document's chunks to  Qdrant 'points'."""
        # 1. First, delete everything old for this file
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.Filter(
                must=[
                    models.FieldCondition(
                        key="file_path",
                        match=models.MatchValue(value=document.file_path),
                    )
                ]
            ),
        )

        # 2. Now we can safely write new ones.
        points = []
        for i, chunk in enumerate(document.chunks):
            # In Qdrant each point to have unique ID (UUID or int)
            point_id = str(chunk.id)

            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=chunk.vector,  # Document.chunks has vectors
                    payload={
                        "text": chunk.content,
                        "file_path": document.file_path,
                        "file_name": document.file_name,
                        "file_hash": document.file_hash,
                        "chunk_index": i,
                        **chunk.metadata,
                    },
                )
            )

        self.client.upsert(collection_name=self.collection_name, points=points)
        print(
            f"[Qdrant] Indexed {len(points)}",
            f"chunks for {document.file_name}",
        )


# OLD VERSION
class InMemoryVectorStoreAdapter:
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
