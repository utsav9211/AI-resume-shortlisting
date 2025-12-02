from src.extract_text import extract_text
from pathlib import Path


def test_extract_txt():
    path = Path('data/resumes_sample/sample1.txt')
    text = extract_text(str(path))
    assert text is not None
    assert 'Experienced backend engineer' in text


