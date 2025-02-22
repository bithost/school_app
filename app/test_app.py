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

def test_create_and_delete_test_record():
    # Test data
    test_data = {
        "field": "Test Record"
    }
    
    # Create record
    create_response = pb.post('/api/collections/test/records', json=test_data)
    assert create_response.status_code == 200
    
    # Get the created record data
    record_data = create_response.json()
    assert record_data['field'] == test_data['field']
    assert 'id' in record_data
    assert 'created' in record_data
    assert 'updated' in record_data
    
    # Store the record ID
    record_id = record_data['id']
    
    # Delete the record
    delete_response = pb.delete(f'/api/collections/test/records/{record_id}')
    assert delete_response.status_code == 204
    
    # Verify the record is deleted
    get_response = pb.get(f'/api/collections/test/records/{record_id}')
    assert get_response.status_code == 404
