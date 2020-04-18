#!/usr/bin/env python3
import bottle
from bottle import get, post, request, run, BaseRequest, response
import json
import game_parser
import game_handler
import game_logger
import models
import os
from os import path
import subprocess
import threading

process = None



def allow_cors(func):
    """ this is a decorator which enable CORS for specified endpoint """
    def wrapper(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*' # * in case you want to be accessed via any website
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return func(*args, **kwargs)
    return wrapper

app = bottle.app()


@app.route('/game_info', method=['OPTIONS', 'POST'])
@allow_cors
def get_game_info():
    game_json = request.json
    # Game Parser is initialized and used to store basic game-information as well as extracted extra information in game_object
    gp = game_parser.GameParser.GameParser()
    game_object = gp.build_json_from_object(gp.build_game_object(game_json))
    return game_object

@app.route('/startGame', method=['GET'])
@allow_cors
def start_game():
    global process
    if not process:
        process = subprocess.Popen('C:\\Users\\Nils\\Documents\\manual_solution\\Server\\ic20_windows.exe -t 0 -u "https://localhost:44381/game"', shell=True)
    else:
        subprocess.check_call("exit", shell=True)
     
    return {"success": "true"}


# CENTRAL AUTO-GAMEMODE ENDPOINT
@app.route('/', method=['OPTIONS', 'POST'])
@allow_cors
def index():
    game_json = request.json
    # Game Parser is initialized and used to store basic game-information as well as extracted extra information in game_object
    gp = game_parser.GameParser.GameParser()
    game_object = gp.build_game_object(game_json)

    # Game Handler is initialized and used to evaluate the current game state and select an action from it
    gh = game_handler.ProceduralGameHandler.ProceduralGameHandler()
    action = gh.evaluateGameAndSelectAction(game_object)
    
    if game_object.basic_game_information.outcome != "pending":
        print(game_object.basic_game_information.outcome)
    return action

BaseRequest.MEMFILE_MAX = 10 * 1024 * 1024
run(host="0.0.0.0", port=50123, quiet=True)
