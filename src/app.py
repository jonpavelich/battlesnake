from flask import Flask, Response, request, send_from_directory
from api import ping_response, start_response, move_response, end_response
from snake import choose_move
from util import get_config
import json
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
config = get_config()
app = Flask(__name__)

"""
Check the vitals
"""
@app.route('/', methods = ['GET', 'POST'])
def route_root():
    return "I'm a snake, and I have good grammar."

"""
Serve a static file for the snake head image
"""
@app.route('/static/<path:path>', methods = ['GET', 'POST'])
def send_static(path):
    return send_from_directory('static', path)

"""
This keeps the snake alive, in case of Heroku
taking an early coffee break.
"""
@app.route('/ping', methods = ['GET', 'POST'])
def ping():
    return ping_response()

"""
Our snake has a very small brain so it's stateless
This just slaps the snake awake
"""
@app.route('/start', methods = ['GET', 'POST'])
def start():
    logging.debug(f"/start request: {request.get_json()}")
    color = config['color']
    headType = config['headType']
    tailType = config['tailType']
    return start_response(color, headType, tailType)

"""
This is called whenever the server wants our next move
It's where the magic happens
"""
@app.route('/move', methods = ['GET', 'POST'])
def move():
    data = request.get_json()
    logging.debug(f"/move request: {data}")
    direction = choose_move(data)
    return move_response(direction)

"""
Just responds with 200 to let the server know it's All Good In The Hood
"""
@app.route('/end', methods = ['GET', 'POST'])
def end():
    data = request.get_json()
    logging.debug(f"/end request: {json.dumps(data)}")
    return end_response()

"""
This is the main function, so you can start the server without asking Flask nicely
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0')
