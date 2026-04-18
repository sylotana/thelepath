## Project Status: What is already done

`tidy(architecture):`

- **Domain Layer**: Core entities (`Document`, `Chunk`) are defined with type safety and automatic ID generation.

- **Port System**: Defined interfaces for File System, Parsing, and Vector Storage, ensuring the "Plug-and-Play" nature of the system.

- **Infrastructure**: Implemented a `LocalFileSystemAdapter` and an `InMemoryVectorStore` for initial testing.

- **Application Layer**: Created the `AddSourceToContextUseCase` which orchestrates the ingestion flow.

- **Tooling & Quality**: Integrated `Ruff` (linting/formatting) and `Mypy` (strict type checking) with a 79-character limit and PEP 8 standards.

- **Environment**: Isolated the project within the `backend/` directory with its own `.venv` and configuration.

---

## Roadmap: The Path to a Functional Local RAG

### Phase 1: Brain Surgery (Making the RAG "Smart")

Focus: Move from "dummy" text handling to actual mathematical representations.

- **Task 1: Implement `FastEmbedAdapter`**
    1. Add `fastembed` to dependencies.
    2. Create `FastEmbedAdapter` in infrastructure.
    3. Download and initialize a lightweight model (e.g., `BAAI/bge-small-en-v1.5`).

- **Task 2: Upgrade Document Parsing**
    1. Modify `ParserAdapter` to utilize the `split_into_chunks` method.
    2. Define default `chunk_size` and `chunk_overlap`.

- **Task 3: Implement Embedding Generation Use Case**
    1. Update the ingestion pipeline to generate vectors for every chunk before saving them to the database.

### Phase 2: Semantic Retrieval (Finding Information)

Focus: Search by meaning, not just by keywords.

- **Task 1: Create `SearchContextUseCase`**
    1. Implement logic to convert a user query into a vector.
    2. Call the Vector Store to find the top-K most similar chunks.

- **Task 2: Persistent Storage**
    1. Swap `InMemoryVectorStore` for a real disk-based adapter (e.g., `LanceDB` or `ChromaDB` persistent mode).

- **Task 3: CLI Search Test**
    1. Update `main.py` to allow "asking" a question and printing the most relevant text snippets from your local files.

### Phase 3: The "G" in RAG (Generation)

Focus: Connect a local LLM to answer questions based on retrieved data.

- **Task 1: Implement `LLMPort` & `OllamaAdapter`**
    1. Connect to a local Ollama instance (running Llama 3 or Mistral).

- **Task 2: Prompt Engineering**
    1. Create a "System Prompt" that forces the AI to answer only using the provided context.

- **Task 3: Complete RAG Loop**
    1. Integrate Retrieval and Generation into a single CLI command.

---

## Next Session Checklist

- [ ] Install dependencies: `uv add fastembed`
- [ ] Define `EmbeddingsPort`: Add the abstract interface to `domain/ports.py`.
- [ ] Create `FastEmbedAdapter`: Implement the actual vector generation logic.
- [ ] Update Ingestion Use Case: Ensure chunks are "vectorized" before being stored.
- [ ] Run Quality Checks: `ruff` & `mypy` must stay green!
