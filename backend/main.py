import sys
from pathlib import Path

# Adding src to sys.path to handle imports correctly if running as a script
sys.path.append(str(Path(__file__).parent.parent))

from src.application.use_cases.add_source import AddSourceToContextUseCase
from src.infrastructure.adapters.file_system import LocalFileSystemAdapter
from src.infrastructure.adapters.parser import SimpleParserAdapter
from src.infrastructure.adapters.vector_store import InMemoryVectorStoreAdapter


def bootstrap() -> None:
    """Composition Root: Wiring everything together."""
    # 1. Initialize Adapters (Infrastructure)
    # We define supported extensions here
    file_system = LocalFileSystemAdapter(
        supported_extensions={".txt", ".md", ".pdf"}
    )
    vector_store = InMemoryVectorStoreAdapter()
    parser = SimpleParserAdapter()

    # 2. Inject Adapters into Use Case (Application)
    use_case = AddSourceToContextUseCase(
        file_system_gateway=file_system,
        vector_store=vector_store,
        parser_service=parser,
    )

    # 3. Simulate a call (In the future, this will be triggered via API/IPC)
    # For testing, let's try to index some local folder or file
    print("--- Starting RAG Ingestion Process ---")

    test_paths = ["./test_data"]  # Make sure this folder exists

    result = use_case.execute(paths=test_paths)

    print(f"--- Process Finished: {result} ---")


if __name__ == "__main__":
    bootstrap()
