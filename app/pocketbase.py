import requests
import os
import time
from functools import wraps

# Try to import from config.py first, fallback to environment variables
try:
    from config import POCKETBASE_ADMIN_EMAIL, POCKETBASE_ADMIN_PASSWORD
except ImportError:
    POCKETBASE_ADMIN_EMAIL = os.getenv('POCKETBASE_ADMIN_EMAIL')
    POCKETBASE_ADMIN_PASSWORD = os.getenv('POCKETBASE_ADMIN_PASSWORD')

class PocketBaseAuth:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.record = None
        self.is_valid = False
        self.token_expiration = 0
        
        if not all([POCKETBASE_ADMIN_EMAIL, POCKETBASE_ADMIN_PASSWORD]):
            raise ValueError("PocketBase credentials not found in config.py or environment variables")

    def is_token_valid(self):
        """Check if the current token is valid"""
        return self.token and time.time() < self.token_expiration

    def refresh_token(self):
        """Refresh the authentication token"""
        if not self.is_token_valid():
            self.auth_with_password()

    def auth_with_password(self):
        """Authenticate with PocketBase using superuser credentials"""
        auth_data = {
            "identity": POCKETBASE_ADMIN_EMAIL,
            "password": POCKETBASE_ADMIN_PASSWORD
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/api/collections/_superusers/auth-with-password',
                json=auth_data
            )
            response.raise_for_status()
            
            auth_result = response.json()
            self.token = auth_result.get('token')
            self.record = auth_result.get('record')
            self.is_valid = bool(self.token)
            
            if self.token:
                self.token_expiration = time.time() + 3600  # Assume 1 hour expiration, adjust as needed
            
            return auth_result
        except requests.exceptions.RequestException as e:
            print(f"Authentication error: {e}")
            self.clear()
            return None

    def get_headers(self):
        """Get headers with auth token if available"""
        headers = {}
        if self.token:
            headers['Authorization'] = self.token
        return headers

    def clear(self):
        """Logout - clear authentication data"""
        self.token = None
        self.record = None
        self.is_valid = False
        self.token_expiration = 0

    def authenticated_request(self, method, url, **kwargs):
        """Wrapper for authenticated requests with token refresh"""
        self.refresh_token()
        headers = self.get_headers()
        kwargs['headers'] = {**kwargs.get('headers', {}), **headers}
        response = requests.request(method, url, **kwargs)
        if response.status_code == 401:  # Unauthorized
            self.refresh_token()
            headers = self.get_headers()
            kwargs['headers'] = {**kwargs.get('headers', {}), **headers}
            response = requests.request(method, url, **kwargs)
        return response

    def get(self, endpoint, **kwargs):
        """Wrapper for GET requests"""
        return self.authenticated_request('GET', f'{self.base_url}{endpoint}', **kwargs)

    def post(self, endpoint, **kwargs):
        """Wrapper for POST requests"""
        return self.authenticated_request('POST', f'{self.base_url}{endpoint}', **kwargs)

    def put(self, endpoint, **kwargs):
        """Wrapper for PUT requests"""
        return self.authenticated_request('PUT', f'{self.base_url}{endpoint}', **kwargs)

    def delete(self, endpoint, **kwargs):
        """Wrapper for DELETE requests"""
        return self.authenticated_request('DELETE', f'{self.base_url}{endpoint}', **kwargs)