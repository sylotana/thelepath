from typing import cast

from fastembed import TextEmbedding


class FastEmbedAdapter:
    """TODO: add correct docstring."""

    def __init__(self, *, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        """Initializes the FastEmbed model.

        The first time this runs, it will download
        the model to your local cache.
        """
        self.model = TextEmbedding(model_name=model_name)

    def get_embeddings(self, *, texts: list[str]) -> list[list[float]]:
        """TODO: add correct docstring."""
        # FastEmbed's .embed() returns an iterable of numpy arrays
        embeddings_generator = self.model.embed(texts)
        return [embedding.tolist() for embedding in embeddings_generator]

    def get_query_embedding(self, *, text: str) -> list[float]:
        """TODO: add correct docstring."""
        # We wrap the single text in a list, then take the first result
        # 1. Get Iterable
        query_iterable = self.model.embed([text])

        # 2. Make it to Iterator
        query_iter = iter(query_iterable)

        # 3. Get first element
        vector = next(query_iter)

        return cast(list[float], vector.tolist())
