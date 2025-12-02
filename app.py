"""
Flask API to score uploaded resumes vs job descriptions.
Endpoints:
- POST /predict : upload file or pass resume_text and job_id
- GET /job_descriptions : list available job descriptions
- GET /health : health check
"""
from flask import Flask, request, jsonify, send_from_directory
import os
from pathlib import Path
import sys

# Add project root to path to import src modules
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.extract_text import extract_text
from src.preprocess import clean_text, extract_keywords
from src.score_resume import score_resume, load_vectorizer
import train_model
from src.utils import init_db, insert_candidate

# load job description and keywords
JOB_DIR = PROJECT_ROOT / "data" / "job_descriptions"
MODELS_DIR = PROJECT_ROOT / "models"
JOB_DEFAULT = JOB_DIR / "job.txt"

app = Flask(__name__)

# initialize database
init_db()

# simple helper to read default job description and extract keywords
def load_job(job_path=JOB_DEFAULT):
    text = job_path.read_text(encoding='utf-8', errors='ignore')
    # extract keywords for matching, we'll parse bullet lines as keywords
    keywords = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('-'):
            keywords.append(line.lstrip('-').strip())
    return text, keywords

job_text, job_keywords = load_job()
vectorizer = None
# try loading vectorizer - training may not have been run
try:
    vectorizer = load_vectorizer()
except Exception as e:
    # Attempt to create a vectorizer automatically if missing - helpful for testing
    print("Vectorizer not found; training a quick TF-IDF vectorizer for local testing...")
    train_model.train_and_save()
    try:
        vectorizer = load_vectorizer()
    except Exception:
        vectorizer = None


    # Add debug logging for incoming requests for diagnostics
    @app.before_request
    def log_request_info():
        try:
            print(f"Incoming request: {request.method} {request.path} from {request.remote_addr}")
        except Exception:
            pass


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/job_descriptions')
def job_descriptions():
    # list job description files
    jobs = [p.name for p in JOB_DIR.glob('*.txt')]
    return jsonify({'job_descriptions': jobs})


@app.route('/predict', methods=['POST'])
def predict():
    # Accept: form-data with 'file' uploaded OR JSON with 'resume_text'
    # Optional: job_filename to choose job description
    if 'job_filename' in request.form:
        jfile = JOB_DIR / request.form['job_filename']
        if jfile.exists():
            jtext = jfile.read_text(encoding='utf-8', errors='ignore')
        else:
            jtext = job_text
    else:
        jtext = job_text
    keywords = job_keywords

    text = None
    filename = None
    name = request.form.get('name', 'Anonymous')
    email = request.form.get('email', '')

    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        # save temp file
        uploads = PROJECT_ROOT / 'tmp_uploads'
        uploads.mkdir(exist_ok=True)
        path = uploads / filename
        file.save(str(path))
        text = extract_text(str(path))
    else:
        # try JSON body
        data = request.get_json(silent=True)
        if data and 'resume_text' in data:
            text = data['resume_text']
    if not text:
        return jsonify({'error': 'No resume provided or failed to extract text'}), 400

    # score
    sv = vectorizer
    if sv is None:
        # try to load again
        try:
            sv = load_vectorizer()
        except Exception as e:
            return jsonify({'error': 'Vectorizer not available; run train_model.py'}), 500

    result = score_resume(text, jtext, keywords, vectorizer=sv)
    # insert to DB
    try:
        insert_candidate(name, email, filename if filename else '', float(result['score']), float(result['similarity']))
    except Exception as e:
        print('db insert failed:', e)

    return jsonify(result)


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 5000)), debug=True)
