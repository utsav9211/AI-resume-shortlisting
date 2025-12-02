import json
from app import app


def test_health():
    client = app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data.get('status') == 'ok'


def test_predict_text():
    client = app.test_client()
    # use short text for resume
    res = client.post('/predict', json={'resume_text': 'python flask sql docker aws'})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert 'score' in data
    assert 'similarity' in data


