"""
Streamlit UI to upload resume, pick job description, and display score & missing skills
"""
import streamlit as st
import requests
from pathlib import Path

# Streamlit secrets may not exist in local dev; handle gracefully and default to localhost
DEFAULT_API_URL = 'http://localhost:5000'
try:
    # Access st.secrets in a guarded way, with safe fallback
    API_URL = DEFAULT_API_URL if not hasattr(st, 'secrets') else st.secrets.get('API_URL', DEFAULT_API_URL)
except Exception:
    # If any error reading secrets, fall back to default
    API_URL = DEFAULT_API_URL

st.title('AI Resume Shortlisting')

# Load job descriptions
JOB_DIR = Path('data/job_descriptions')
jobs = [p.name for p in JOB_DIR.glob('*.txt')]

job_choice = st.selectbox('Select job description', jobs)
job_text = (JOB_DIR / job_choice).read_text(encoding='utf-8', errors='ignore')

st.header('Job Description')
st.write(job_text)

st.header('Upload Resume')
uploaded_file = st.file_uploader('Upload resume (PDF/DOCX/TXT) or paste text below', type=['pdf', 'docx', 'txt'])
resume_text_area = st.text_area('Or paste resume text here (optional)')

name = st.text_input('Candidate Name')
email = st.text_input('Candidate Email')

if st.button('Score Resume'):
    if uploaded_file is None and not resume_text_area:
        st.warning('Please upload a file or paste resume text')
    else:
        files = None
        data = {'job_filename': job_choice, 'name': name or 'Anonymous', 'email': email or ''}
        if uploaded_file is not None:
            files = {'file': (uploaded_file.name, uploaded_file.read())}

        # call API
        try:
            if files:
                resp = requests.post(f"{API_URL}/predict", data=data, files=files)
            else:
                resp = requests.post(f"{API_URL}/predict", json={'resume_text': resume_text_area, 'name': name, 'email': email, 'job_filename': job_choice})
            if resp.status_code == 200:
                result = resp.json()
                st.success(f"Score: {result.get('score', 'N/A')}")
                st.write('Similarity: ', result.get('similarity', 'N/A'))
                st.write('Missing skills: ', result.get('missing_skills', []))
                st.write('Detected resume skills: ', result.get('resume_skills', []))
            else:
                st.error(f"API error: {resp.status_code} - {resp.text}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")

