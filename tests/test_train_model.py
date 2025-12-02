from train_model import train_and_save
from pathlib import Path


def test_train_and_save_creates_file():
    out = Path('models/tfidf_vectorizer.joblib')
    if out.exists():
        out.unlink()
    train_and_save()
    assert out.exists()


