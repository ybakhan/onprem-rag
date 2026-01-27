import os
from pathlib import Path
from app.core.indexer import index_embed_pdf


def index_dir(directory_path=None, lang=None):
    """Index all PDF files in the specified directory."""

    directory_path = directory_path or os.getenv("CONTENT_DIR", "./tests/docs/en")
    lang = lang or os.getenv("CONTENT_LANG", "en")

    print(f"Indexing PDF files in: {directory_path}")
    print("-" * 50)

    directory = Path(directory_path).resolve()

    for path in directory.iterdir():
        if (
            path.is_file()
            and path.suffix.lower() == ".pdf"
            and not path.name.startswith(".")
        ):
            index_embed_pdf(path, lang)


if __name__ == "__main__":
    index_dir()
