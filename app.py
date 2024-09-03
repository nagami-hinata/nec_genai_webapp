# app.py
from flask import Flask, send_from_directory
import os

app = Flask(__name__)

APP_FILES_DIR = 'app_files'  # アプリファイルを格納するディレクトリ名

@app.route('/')
def home():
    return send_from_directory(APP_FILES_DIR, 'index.html')

@app.route('/<path:path>')
def send_app_files(path):
    return send_from_directory(APP_FILES_DIR, path)

if __name__ == '__main__':
    app.run(debug=True)