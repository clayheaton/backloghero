"""
Initializes the Flask app in a manner that works well with nginx
"""
from backloghero import app
import os

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
