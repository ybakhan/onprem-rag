from pathlib import Path
from app.core.indexer import index_embed_pdf


def index_dir(directory_path):
    """Index all PDF files in the specified directory."""
    print(f"Indexing PDF files in: {directory_path}")
    print("-" * 50)

    directory = Path(directory_path).resolve()

    for path in directory.iterdir():
        if (
            path.is_file()
            and path.suffix.lower() == ".pdf"
            and not path.name.startswith(".")
        ):
            index_embed_pdf(path)


index_dir("./tests/docs/en")
index_dir("./tests/docs/ar")
