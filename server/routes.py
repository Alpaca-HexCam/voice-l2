from server import app
from flask import request, jsonify

@app.route('/')
@app.route('/index') #www.alapaca.com/index
def index():
    return "hello world"




#www.alpaca.com/ -> hello world
#www.alpaca.com/index -> hellow world
