import os
from flask import Flask, render_template
from flask_misaka import Misaka
from datetime import datetime

app = Flask(__name__)
Misaka(app)

# Custom Jinja filter for formatting dates
def format_date(value, format='%b %d, %Y'):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').strftime(format)

app.jinja_env.filters['format_date'] = format_date

# Hardcoded data for demonstration purposes
ABOUT_DATA = {
    "title": "About Us",
    "content": "This is a simple about page loaded from a local template."
}

ARTICLES = [
    {"id": 1, "title": "First Article", "date": "2023-01-01T12:00:00.000Z", "summary": "This is the first article."},
    {"id": 2, "title": "Second Article", "date": "2023-02-01T12:00:00.000Z", "summary": "This is the second article."},
    {"id": 3, "title": "Third Article", "date": "2023-03-01T12:00:00.000Z", "summary": "This is the third article."}
]

@app.route('/about')
def about():
    # Pass the hardcoded about data to the template
    return render_template('about.html', data=ABOUT_DATA)

@app.route('/')
def home():
    # Pass the hardcoded articles data to the template
    return render_template('index.html', articles=ARTICLES)

@app.route('/article/<int:article_id>')
def read_article(article_id):
    # Find the article with the matching ID in the hardcoded data
    article_data = next((article for article in ARTICLES if article["id"] == article_id), None)

    if article_data:
        # Render the template with the article data
        return render_template('article.html', article_data=article_data)
    else:
        # Handle the case where the article is not found
        return f"Error: Article with ID {article_id} not found.", 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
