import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from ScrumPokerTablePy.config import *
from ScrumPokerTablePy.queue import EventQueue

app = Flask(__name__)
app.config.from_object('ScrumPokerTablePy.config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.sqlite')

db = SQLAlchemy(app)
api = Api(app)

events = EventQueue()

import ScrumPokerTablePy.server