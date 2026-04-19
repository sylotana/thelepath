from typing import Any

from src.domain.ports import (
    EmbeddingsPort,
    FileSystemPort,
    ParserPort,
    VectorStorePort,
)


class AddSourceToContextUseCase:
    """TODO: add correct docstring."""

    def __init__(
        self,
        *,
        file_system_gateway: FileSystemPort,
        vector_store: VectorStorePort,
        parser_service: ParserPort,
        embeddings_service: EmbeddingsPort,
    ) -> None:
        """TODO: add correct docstring."""
        self.file_system = file_system_gateway
        self.vector_store = vector_store
        self.parser = parser_service
        self.embeddings = embeddings_service

    def execute(self, *, paths: list[str]) -> dict[str, Any]:
        """Main scenario to add sources to the context."""
        # 1. Resolve directories into a flat list of paths
        all_file_paths = self.file_system.resolve_all_files(paths=paths)

        # 2. Filter for supported file types only
        valid_paths = [
            p for p in all_file_paths if self.file_system.is_supported(path=p)
        ]

        processed_count = 0
        for path in valid_paths:
            # Calculate the file hash in advance to pass it for verification
            file_hash = self.file_system.get_file_hash(path=path)

            # 3. Check if an update is required (hash check)
            if not self.vector_store.needs_update(
                file_path=path, file_hash=file_hash
            ):
                continue

            # 4. Parse the file into a Document domain entity
            # Pass the hash directly so it is included in the Document entity
            document = self.parser.parse_to_document(
                path=path, file_hash=file_hash
            )

            # 5. Domain logic: Chunking
            document.split_into_chunks()

            if not document.chunks:
                continue

            # 6. Get embeddings (batch)
            vectors = self.embeddings.get_embeddings(
                texts=document.text_batches
            )

            # 7. Update chunks use vectors
            document.vectorize(vectors=vectors)

            # 8. Save
            self.vector_store.index_document(document=document)
            processed_count += 1

        return {
            "status": "completed",
            "total_found": len(valid_paths),
            "files_indexed": processed_count,
        }
