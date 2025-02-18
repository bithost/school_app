from app import app, pb
import pytest
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_app_running():
    assert app.name == 'app'

def test_create_and_delete_test_record(client):
    # Test data
    test_data = {
        "title": "Test Record",
        "description": "This is a test record"
    }
    
    # Create record
    create_response = client.post('/api/collections/test/records', json=test_data)
    assert create_response.status_code == 200
    
    # Get the created record data
    record_data = create_response.json()
    assert record_data['title'] == test_data['title']
    assert record_data['description'] == test_data['description']
    
    # Store the record ID
    record_id = record_data['id']
    
    # Delete the record
    delete_response = client.delete(f'/api/collections/test/records/{record_id}')
    assert delete_response.status_code == 204
    
    # Verify the record is deleted
    get_response = client.get(f'/api/collections/test/records/{record_id}')
    assert get_response.status_code == 404
