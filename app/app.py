# app.py

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Dockerized Flask App Behind Load Balancer!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
