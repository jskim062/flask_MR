
import flask_MR1
from flask_MR1 import app
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hi(client):
    response = client.get('/hi')
    assert response.status_code == 200
    assert b'hi, World!' in response.data


def test_echo(client):
    data = {'message': 'pytest'}
    response = client.post('/echo', json=data)
    assert response.status_code == 200
    assert response.get_json() == data


def test_upload_image(client):
    from PIL import Image
    import io
    img = Image.new('RGB', (123, 456), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    data = {'file': (img_bytes, 'test.png')}
    response = client.post('/upload_image', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert response.get_json() == {"width": 123, "height": 456}


def test_predict_score(client, monkeypatch):
    class DummyModel:
        def predict(self, X):
            return [42.0]
    monkeypatch.setattr('flask_MR1.loaded_model1', DummyModel())
    response = client.get('/predict_score?horus=3.0')
    assert response.status_code == 200
    assert response.get_json() == {"prediction": 42.0}


def test_predict_image(client, monkeypatch):
    from PIL import Image
    import io
    import numpy as np

    class DummyKerasModel:
        def predict(self, img_array):
            return [[60.0]]  # 또는 [[np.float32(60)]]
    monkeypatch.setattr(flask_MR1, "loaded_model", DummyKerasModel())
    img = Image.new('RGB', (180, 180), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    data = {'file': (img_bytes, 'test.png')}
    response = client.post('/predict_image', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert response.get_json() == {"predict_result": "cat"}
