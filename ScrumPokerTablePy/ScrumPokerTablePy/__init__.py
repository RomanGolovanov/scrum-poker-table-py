import os
from threading import Thread

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from ScrumPokerTablePy.config import *
from flask_socketio import SocketIO

app = Flask(__name__)
app.debug = True
app.config.from_object('ScrumPokerTablePy.config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.sqlite')
app.config['SECRET_KEY'] = '8019234jkll1j2;j4nx8934c8!'


db = SQLAlchemy(app)
api = Api(app)
socketio = SocketIO(app)
thread = None

import ScrumPokerTablePy.server