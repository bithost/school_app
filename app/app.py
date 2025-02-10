# app.py
import os
from flask import Flask, render_template, jsonify
from datetime import datetime
import requests
from pocketbase import PocketBaseAuth
from config import *

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
    endpoint = f'{pb.base_url}/api/collections/posts/records'
    
    try:
        response = requests.get(endpoint, headers=pb.get_headers())
        response.raise_for_status()
        posts = response.json()
        return render_template('index.html', posts=posts.get('items', []))
    except Exception as e:
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
