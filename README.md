# AI Resume Shortlisting

A minimal AI Resume Shortlisting System using TF-IDF + Cosine Similarity.

This project implements a Flask API for scoring resumes against job descriptions and a Streamlit UI to upload resumes and view scores.

Key features:
- Resume text extraction (PDF, DOCX, TXT)
- TF-IDF vectorizer and cosine similarity based scoring
- SQLite-backed minimal candidate store
- Flask REST endpoint and Streamlit frontend
- Model saving with joblib

Quick start:
1. Create a Python 3.10+ virtual environment
2. Install dependencies: pip install -r requirements.txt
3. Train vectorizer: python train_model.py
4. Start API: python app.py
5. Start Streamlit UI: streamlit run streamlit_app.py
Run tests:
```
pytest -q
```

Acceptance test (curl):
```
curl -F "file=@data/resumes_sample/sample1.txt" http://localhost:5000/predict
```

Expected JSON format (example):
```
{
	"score": 83.47,
	"similarity": 0.8347,
	"missing_skills": ["kubernetes"],
	"resume_skills": ["python","flask","sql"]
}
```

Notes:
- If you want to use sentence-transformers (SBERT) instead of TF-IDF, see comments in `src/score_resume.py`.
- The Streamlit UI calls the API at `http://localhost:5000` by default. Set `st.secrets['API_URL']` to a different URL if needed.
 - The Streamlit UI calls the API at `http://localhost:5000` by default. Set `st.secrets['API_URL']` to a different URL if needed.
 
Note on IPv6/IPv4 bindings: `localhost` may resolve to `::1` (IPv6) or `127.0.0.1` (IPv4). On macOS, other services (e.g., AirPlay/AirTunes) may be bound to port 5000 on IPv6 and return 403. If `curl` returns a 403 or you see that your requests are not reaching Flask, use 127.0.0.1 explicitly or force IPv4:

```bash
curl -4 -v -F "file=@data/resumes_sample/sample1.txt" http://127.0.0.1:5000/predict
```

You can also explicitly bind Flask to IPv4 (127.0.0.1) when running the app:

```bash
python -c "from app import app; app.run(host='127.0.0.1', port=5000, debug=True)"
```

Diagnostic command to see which process is listening on port 5000:

```bash
lsof -iTCP -sTCP:LISTEN -n -P | grep 5000
# or macOS:
# sudo lsof -i :5000
```

If you see another process (e.g., AirPlay/AirTunes) listening on port 5000, either stop that service or use a different port for your app (e.g., 5001) by setting `PORT` environment variable before running the app:

```bash
export PORT=5001
python app.py
```

Streamlit secrets (optional):
If you'd rather configure the API URL via Streamlit secrets, create `.streamlit/secrets.toml`: 
```
API_URL = "http://localhost:5000"
```
Streamlit will automatically pick that up. The app falls back to the default `http://localhost:5000` if no secrets are present.

For more details, read next sections and the comments in each file.
