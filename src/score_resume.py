"""
Scoring logic: transform resume and job to TF-IDF vectors and compute cosine similarity.
"""
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from joblib import load
from pathlib import Path
from typing import Dict, Any, List, Set
from .preprocess import extract_keywords, tokenize


MODELS_DIR = Path(__file__).resolve().parent.parent / "models"


def load_vectorizer(path: str = None):
    """Load the TF-IDF vectorizer saved with joblib"""
    if path is None:
        path = MODELS_DIR / "tfidf_vectorizer.joblib"
    return load(path)


def score_resume(resume_text: str, job_text: str, keywords: List[str], vectorizer=None) -> Dict[str, Any]:
    """Compute cosine similarity and missing skills between job_text and resume_text

    Returns dict with 'similarity' (float) and 'missing_skills' (List[str]) and 'resume_skills'
    """
    if vectorizer is None:
        vectorizer = load_vectorizer()
    # vectorize
    tfidf = vectorizer.transform([resume_text, job_text])
    sim = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
    # skills
    job_keywords = set([k.lower() for k in keywords])
    resume_skills = extract_keywords(resume_text, keywords)
    missing = sorted(list(job_keywords - set([s.lower() for s in resume_skills])))

    # give a score out of 100
    score = float(round(sim * 100, 2))
    return {
        "similarity": sim,
        "score": score,
        "missing_skills": missing,
        "resume_skills": sorted([s.lower() for s in resume_skills])
    }


# optional function to batch score multiple resumes
def score_batch(resume_texts: List[str], job_text: str, keywords: List[str], vectorizer=None):
    if vectorizer is None:
        vectorizer = load_vectorizer()
    tfidf = vectorizer.transform([job_text] + resume_texts)
    job_vec = tfidf[0:1]
    result = []
    sims = cosine_similarity(tfidf[1:], job_vec).reshape(-1)
    for idx, txt in enumerate(resume_texts):
        res = {
            "index": idx,
            "similarity": float(sims[idx]),
            "score": float(round(sims[idx] * 100, 2)),
            "resume_skills": sorted(list(extract_keywords(txt, keywords)))
        }
        res["missing_skills"] = sorted(list(set([k.lower() for k in keywords]) - set(res["resume_skills"])))
        result.append(res)
    return result


# NOTE: Optional - if you want to use SBERT (sentence-transformers) instead of TF-IDF,
# uncomment and use the compute_score_sbert helper below and install sentence-transformers.
#
# from sentence_transformers import SentenceTransformer
# def compute_score_sbert(resume_text: str, job_text: str, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
#     model = SentenceTransformer(model_name)
#     vecs = model.encode([resume_text, job_text])
#     sim = float(cosine_similarity([vecs[0]], [vecs[1]])[0][0])
#     return sim
