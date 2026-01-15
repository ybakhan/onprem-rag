# tests/test_user_service.py
import shutil
from pathlib import Path
import pytest
import deepl
from _pytest.monkeypatch import MonkeyPatch
from app.core.indexer import index_embed_pdf
from app.config import settings
from app.core.chat_completion_local import chat_completion_local
from app.core.chat_completion import chat_completion
from deepl.api_data import ModelType
from util.translate import to_english
from util.translate import to_arabic

@pytest.fixture(scope="module", autouse=True)
def setup():
    document_store_dir = Path(__file__).parent / "storage"
    if document_store_dir.exists():
        shutil.rmtree(document_store_dir, ignore_errors=True)

    mp = MonkeyPatch()
    mp.setattr(settings, "DOCUMENT_STORE_DIR", str(document_store_dir))
    mp.setattr(settings, "VECTOR_DB_PATH", str(document_store_dir / "chromadb"))

    yield

    mp.undo()
    shutil.rmtree(document_store_dir, ignore_errors=True)


@pytest.mark.parametrize(
    "lang, question",
    [
        ("en", "How to access health care in Canda?"),
        ("ar", "كيف يمكن الحصول على الرعاية الصحية في كندا؟")
    ],
)
def test_index_embed(lang, question):
    document_path = str(Path(__file__).parent / "docs" / lang / f"health-care-{lang}.pdf")

    documents = index_embed_pdf(document_path)
    assert len(documents) > 0

    # indexing of same document should be skipped
    documents = index_embed_pdf(document_path)
    assert len(documents) == 0

    answer = chat_completion(question, lang)
    # answer = chat_completion_local(question, lang)
    assert len(answer) > 0

    if lang == "ar":
        result = to_english(answer)
        print(result.text)
    else:
        print(answer)
