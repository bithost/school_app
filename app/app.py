# app.py
from flask import Flask, render_template, jsonify, request
from datetime import datetime
import requests
from pocketbase import PocketBaseAuth
import os
import logging

# Configure logging to only show access logs without request body
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

# Try to import from config.py first, fallback to environment variables
try:
    from config import POCKETBASE_URL
except ImportError:
    POCKETBASE_URL = os.getenv('POCKETBASE_URL')

if not POCKETBASE_URL:
    raise ValueError("POCKETBASE_URL not found in config.py or environment variables")

app = Flask(__name__)

# Initialize PocketBase and authenticate
pb = PocketBaseAuth(POCKETBASE_URL)
auth_result = pb.auth_with_password()

if not auth_result:
    print("Failed to authenticate with PocketBase")

# Custom Jinja filter for formatting dates
def format_date(value, format='%b %d, %Y'):
    try:
        # First try ISO format
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').strftime(format)
    except ValueError:
        try:
            # Then try PocketBase format
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%fZ').strftime(format)
        except ValueError as e:
            print(f"Error parsing date {value}: {e}")
            return value

app.jinja_env.filters['format_date'] = format_date

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    endpoint = f'{pb.base_url}/api/collections/posts/records'
    
    try:
        params = {
            'page': page,
            'perPage': per_page,
            'sort': '-created'
        }
        response = requests.get(endpoint, headers=pb.get_headers(), params=params)
        response.raise_for_status()
        data = response.json()
        posts = data.get('items', [])
        total_items = data.get('totalItems', 0)
        total_pages = -(-total_items // per_page)  # Ceiling division
        
        print(f"Total items: {total_items}")
        print(f"Total pages: {total_pages}")
        print(f"Current page: {page}")
        print(f"Number of posts on this page: {len(posts)}")
        
        return render_template('index.html', posts=posts, page=page, total_pages=total_pages)
    except Exception as e:
        print(f"Error: {str(e)}")
        return f'Error: {str(e)}', 500

@app.route('/post/<string:id>')
def view_post(id):
    endpoint = f'{pb.base_url}/api/collections/posts/records/{id}'
    
    try:
        response = requests.get(endpoint, headers=pb.get_headers())
        response.raise_for_status()
        post = response.json()
        return render_template('article.html', post=post)
    except Exception as e:
        return f'Error: {str(e)}', 500

@app.route('/about')
def about():
    endpoint = f'{pb.base_url}/api/collections/about/records'
    response = requests.get(endpoint, headers=pb.get_headers())
    if response.status_code == 200:
        # Get the first record since we only have one
        about_data = response.json()['items'][0] if response.json()['items'] else None
        return render_template('about.html', about=about_data)
    return 'Error loading about page', 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
