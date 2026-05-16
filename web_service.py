from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
