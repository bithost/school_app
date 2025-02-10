import requests
from config import POCKETBASE_ADMIN_EMAIL, POCKETBASE_ADMIN_PASSWORD

class PocketBaseAuth:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.record = None
        self.is_valid = False

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
