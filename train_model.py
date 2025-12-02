"""
Train a TF-IDF vectorizer over job descriptions and sample resumes and save to models/tfidf_vectorizer.joblib
"""
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump
import os

DATA_DIR = Path(__file__).parent / "data"
JOB_DIR = DATA_DIR / "job_descriptions"
RESUME_DIR = DATA_DIR / "resumes_sample"
MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)


def gather_corpus():
    corpus = []
    for path in JOB_DIR.glob("*.txt"):
        corpus.append(path.read_text(encoding="utf-8", errors="ignore"))
    for path in RESUME_DIR.glob("*.txt"):
        corpus.append(path.read_text(encoding="utf-8", errors="ignore"))
    # If corpus is empty, add a placeholder to avoid error
    if not corpus:
        corpus.append("sample placeholder text for training vectorizer")
    return corpus


def train_and_save(output_path=str(MODELS_DIR / "tfidf_vectorizer.joblib")):
    corpus = gather_corpus()
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', max_features=5000)
    vectorizer.fit(corpus)
    dump(vectorizer, output_path)
    print(f"Saved TF-IDF vectorizer to: {output_path}")


if __name__ == '__main__':
    train_and_save()
