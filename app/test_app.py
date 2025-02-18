from app import app

def test_home_page():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_app_running():
    assert app.name == 'app'
