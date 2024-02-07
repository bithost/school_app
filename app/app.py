# app.py
import os
from flask import Flask, render_template, jsonify
from datetime import datetime
import requests

app = Flask(__name__)
STRAPI_API_URL = 'https://strapi.lanlab.xyz/api'

STRAPI_API_TOKEN='5cc4f9db84769529632f107a0127b2235be670a97cdd58d1f815f736b1580ad9aac0b39885b119f7c4dca7e6352da1a028cc4c14aaf583df8e807e8ba0f07be6afd63d23bf2db5397d273c3c425bad2c574733d8fdf4e44ee8c80cccd62ae1f498def679c7f0573eacb7885422ae5d8b17dc6a72959ac3e39785cb6eebbbe9fb'
#STRAPI_API_TOKEN = os.environ.get('STRAPI_API_TOKEN')

# Custom Jinja filter for formatting dates
def format_date(value, format='%b %d, %Y'):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').strftime(format)

app.jinja_env.filters['format_date'] = format_date
 
@app.route('/about')
def about():
    # Example endpoint for fetching about data, replace with your actual Strapi endpoint
    endpoint = f'{STRAPI_API_URL}/about'

    # Set up headers with the API token
    headers = {
        'Authorization': f'Bearer {STRAPI_API_TOKEN}'
    }

    # Make a GET request to the Strapi endpoint with headers
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        about_data = response.json()
        # Pass the about data to the template
        return render_template('about.html', data=about_data)
    else:
        # If the request was not successful, handle the error (you can customize this part)
        return f'Error: {response.status_code} - {response.text}'

@app.route('/')
def home():
    # Example endpoint for fetching articles, replace with your actual Strapi endpoint
    endpoint = f'{STRAPI_API_URL}/articles'

    # Set up headers with the API token
    headers = {
        'Authorization': f'Bearer {STRAPI_API_TOKEN}'
    }

    # Make a GET request to the Strapi endpoint with headers
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        articles = response.json()
        # Pass the articles data to the template
        return render_template('index.html', articles=articles)
    else:
        # If the request was not successful, handle the error (you can customize this part)
        return f'Error: {response.status_code} - {response.text}'

@app.route('/article/<int:article_id>')
def read_article(article_id):
    # Replace with actual Strapi API endpoint for fetching a specific article
    strapi_endpoint = f'{STRAPI_API_URL}/articles/{article_id}'

    # Set up headers with the API token
    headers = {
        'Authorization': f'Bearer {STRAPI_API_TOKEN}'
    }

    # Make a GET request to the Strapi endpoint with headers
    response = requests.get(strapi_endpoint, headers=headers)

    try:
        # Parse the JSON response
        article_data = response.json()
    except ValueError as e:
        # Handle JSON parsing error (you can customize this part)
        return f'Error parsing JSON: {e}'

    # Render the template with the article data
    return render_template('article.html', article_data=article_data)














# @app.route('/')
# def home():
#     return render_template('index.html')





# @app.route('/admin')
# def admin():
#     return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
