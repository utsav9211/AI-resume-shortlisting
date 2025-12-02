from src.score_resume import score_resume, load_vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


def test_score_identical_texts():
    # This tests scoring of identical text should produce similarity 1.0
    text = "python flask sql docker aws"
    try:
        vectorizer = load_vectorizer()
    except Exception:
        # fallback to an in-memory vectorizer
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
        vectorizer.fit([text])
    res = score_resume(text, text, keywords=['python'], vectorizer=vectorizer)
    assert res['similarity'] >= 0.99
    assert res['score'] >= 99.0


