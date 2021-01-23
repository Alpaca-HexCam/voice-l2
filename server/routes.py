from server import app
from flask import request, jsonify

@app.route('/')
@app.route('/index') #www.alapaca.com/index
def index():
    data = {'my_data': 'data'}
    return jsonify(data)
