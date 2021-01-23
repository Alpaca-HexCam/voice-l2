from app import app
from flask import request, jsonify

@app.route('/')
@app.route('/index') #www.alapaca.com/index
def index():
    return "Hello, World!"
