import os
import time
from threading import Thread

from ScrumPokerTablePy import api, app, db, thread, socketio
from ScrumPokerTablePy.resources import GameDeskList, GameDesk, Player, GameDeskStart, GameDeskFinish, GameDeskHistory

api.add_resource(GameDeskList, '/api/desk')
api.add_resource(GameDesk, '/api/desk/<string:desk_id>')
api.add_resource(GameDeskStart, '/api/desk/start/<string:desk_id>')
api.add_resource(GameDeskFinish, '/api/desk/finish/<string:desk_id>')
api.add_resource(GameDeskHistory, '/api/desk/history/<string:desk_id>')

api.add_resource(Player, '/api/desk/<string:desk_id>/player/<string:player_name>')

db.create_all()

@app.route('/')
def client_root():
    return app.send_static_file('index.html')


@app.route('/app/<path:path>')
def client_app(path):
    full_path = os.path.join('app/', path)
    return app.send_static_file(full_path)


@app.route('/components/<path:path>')
def client_components(path):
    full_path = os.path.join('components/', path)
    return app.send_static_file(full_path)

