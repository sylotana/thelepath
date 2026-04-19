import sys
from pathlib import Path

# Adding src to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from src.application.use_cases.add_source import AddSourceToContextUseCase
from src.infrastructure.adapters.fastembed import (
    FastEmbedAdapter,
)
from src.infrastructure.adapters.file_system import LocalFileSystemAdapter
from src.infrastructure.adapters.parser import SimpleParserAdapter
from src.infrastructure.adapters.vector_store import (
    QdrantVectorStoreAdapter,
)


def bootstrap() -> None:
    """Composition Root: Wiring everything together."""
    # 1. Initialize Adapters (Infrastructure)
    file_system = LocalFileSystemAdapter(
        supported_extensions={".txt", ".md"}  # Keeping it simple for now
    )

    # Using local storage for Qdrant so it persists in a folder
    vector_store = QdrantVectorStoreAdapter(path="./qdrant_data")

    # The "Smart" part
    embeddings = FastEmbedAdapter(model_name="BAAI/bge-small-en-v1.5")

    parser = SimpleParserAdapter()

    # 2. Inject Adapters into Use Case (Application)
    # Note: Ensure your Use Case __init__ now accepts embeddings_service!
    use_case = AddSourceToContextUseCase(
        file_system_gateway=file_system,
        vector_store=vector_store,
        parser_service=parser,
        embeddings_service=embeddings,  # New Injection
    )

    # 3. Execution
    print("--- Starting RAG Ingestion Process ---")

    test_paths = ["./test_data"]

    # Create the folder if it doesn't exist so it doesn't crash
    Path("./test_data").mkdir(exist_ok=True)

    result = use_case.execute(paths=test_paths)

    print(f"--- Process Finished: {result} ---")


if __name__ == "__main__":
    bootstrap()
