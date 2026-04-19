import hashlib
from pathlib import Path


class LocalFileSystemAdapter:
    """TODO: add correct docstring."""

    def __init__(self, *, supported_extensions: set[str]) -> None:
        """TODO: add correct docstring."""
        self.supported_extensions = supported_extensions

    def resolve_all_files(self, *, paths: list[str]) -> list[str]:
        """Resolve a list of paths into a flat list of files.

        This method processes both individual files and directories,
        searching recursively for all files within them.
        """
        resolved = []
        for p in paths:
            path = Path(p)
            if path.is_file():
                resolved.append(str(path.absolute()))
            elif path.is_dir():
                # Recursively search for all files
                for file in path.rglob("*"):
                    if file.is_file():
                        resolved.append(str(file.absolute()))
        return resolved

    def is_supported(self, *, path: str) -> bool:
        """Checks if the file extension is supported for reading."""
        return Path(path).suffix.lower() in self.supported_extensions

    def get_file_hash(self, *, path: str) -> str:
        """Calculate the SHA256 hash of a file.

        This hash is used to determine if the file content has changed
        since the last check.
        """
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            # Read in chunks to avoid consuming all memory for large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
