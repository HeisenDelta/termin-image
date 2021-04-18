from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
import json
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

# Getting the library directory

try: 
    from ..library.main import function_main, function_main_api
    from ..library.profile import function_profile_api

except (ModuleNotFoundError, ImportError):

    lib = os.path.dirname(os.getcwd()) + '/library'
    sys.path.insert(1, lib)

    from main import function_main, function_main_api
    from profile import function_profile_api


app = Flask(__name__)

@app.route('/')
def main(): return jsonify({ 'output': 'Head over to /api/ to get the strings' })

@app.route('/main/env', methods = ['GET', 'POST'])
def route_main_env():
    if request.method == 'GET':
        env_path = request.args.get('env_path', None)           # Path to env file

        # Added error handling if path is not defined
        try: 
            return jsonify({ 
                'output': function_main(env_path) 
            })

        except FileNotFoundError:
            return jsonify({ 
                'error': f'Path [{env_path}] is not defined' 
            })


@app.route('/main/mnl', methods = ['GET', 'POST'])
def route_main_mnl():
    if request.method == 'GET':
        img_path = request.args.get('img_path', None)           # Path to image file
        color = request.args.get('color', None)
        factor = request.args.get('factor', None)
        orient = request.args.get('orient', None)

        return jsonify({ 
            'output': function_main_api(img_path, color, float(factor), orient)
        })


@app.route('/profile/env', methods = ['GET', 'POST'])
def route_profile_env():
    if request.method == 'GET':
        env_path = request.args.get('env_path', None)           # Path to env file

        load_dotenv(dotenv_path = Path(env_path))
        X_OFFSET = os.getenv('X_OFFSET', None)
        Y_OFFSET = os.getenv('Y_OFFSET', None)

        return jsonify({ 
            'output': function_profile_api(env_path, int(X_OFFSET), int(Y_OFFSET), same_path = False) 
        })


@app.route('/profile/mnl', methods = ['GET', 'POST'])
def route_profile_mnl():
    if request.method == 'GET': 
        img_path = request.args.get('img_path', None)           # Path to image file
        x_offset = request.args.get('x', None)
        y_offset = request.args.get('y', None)
        color = request.args.get('color', None)
        factor = request.args.get('factor', None)

        return jsonify({ 
            'output': function_profile_api(
                img_path, int(x_offset), int(y_offset), same_path = True, COLOR = color, FACTOR = float(factor)
            ) 
        })


@app.route('/details/env', methods = ['GET', 'POST'])
def route_details_mnl():
    if request.method == 'GET':
        env_path = request.args.get('env_path', None)           # Path to env file
        det_path = request.args.get('det_path', None)           # Path to details file


# Error handling exceptions
@app.errorhandler(HTTPException)
def handle_http_ex(e):

    response = e.get_response()
    response.data = json.dumps({
        'code': e.code,
        'name': e.name,
        'description': e.description
    })

    response.content_type = "application/json"
    return response


if __name__ == '__main__': app.run(debug = True)
