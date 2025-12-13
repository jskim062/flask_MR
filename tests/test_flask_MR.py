import pytest
from flask_MR.py import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello(client):
    response = client.get('/hello')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data


def test_echo(client):
    data = {'message': 'pytest'}
    response = client.post('/echo', json=data)
    assert response.status_code == 200
    assert response.get_json() == data


def test_upload_image(client):
    # PIL로 테스트용 이미지 생성
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
    # loaded_model1이 실제로 존재하지 않으니, monkeypatch로 모의 객체 사용
    class DummyModel:
        def predict(self, X):
            return [42.0]
    monkeypatch.setattr('app.loaded_model1', DummyModel())
    response = client.get('/predict_score?horus=3.0')
    assert response.status_code == 200
    assert response.get_json() == {"prediction": 42.0}


def test_predict_image(client, monkeypatch):
    # loaded_model이 실제로 존재하지 않으니, monkeypatch로 모의 객체 사용
    from PIL import Image
    import io

    class DummyKerasModel:
        def predict(self, img_array):
            return [[60]]  # score > 50 이므로 'cat'

    monkeypatch.setattr('app.loaded_model', DummyKerasModel())

    img = Image.new('RGB', (180, 180), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    data = {'file': (img_bytes, 'test.png')}
    response = client.post('/predict_image', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert response.get_json() == {"predict_result": "cat"}
