from flask import Flask, request
import json
import sys
import os

# Getting the library directory
lib = os.path.dirname(os.getcwd()) + '/library'
sys.path.insert(1, lib)

from main import function_main, function_main_mnl

app = Flask(__name__)

@app.route('/')
def main(): return json.dumps({ 'output': 'Head over to /api/ to get the strings' }, indent = 4)

@app.route('/api/env/', methods = ['GET', 'POST'])
def route_env():
    if request.method == 'GET':
        path = request.args.get('path', None)

        return json.dumps({ 'output': function_main(path) }, indent = 4)

@app.route('/api/mnl/', methods = ['GET', 'POST'])
def route_mnl():
    if request.method == 'GET':
        path = request.args.get('path', None)
        color = request.args.get('color', None)
        factor = request.args.get('factor', None)

        return json.dumps({ 'output': function_main_mnl(path, color, float(factor)) }, indent = 4)


if __name__ == '__main__': app.run(debug = True)
