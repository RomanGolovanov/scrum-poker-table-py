from enum import IntEnum

from ScrumPokerTablePy import db

from sqlalchemy_utils import JSONType



class GameDeskStateEnum(IntEnum):
    Waiting = 1
    Voting = 2
    Display = 3


class GameDeskHistoryEntity(db.Model):
    desk_history_id = db.Column(db.Integer, primary_key=True)
    desk_id = db.Column(db.String)
    modified = db.Column(db.Integer)
    content = db.Column(JSONType)

    def __init__(self, desk_id, modified, content):
        self.desk_id = desk_id
        self.modified = modified
        self.content = content

    def __repr__(self):
        return '<GameDeskHistory %r>' % self.desk_history_id


class GameDeskEntity(db.Model):
    desk_id = db.Column(db.String, primary_key=True)
    modified = db.Column(db.Integer)
    state = db.Column(db.Integer)
    cards = db.Column(JSONType)

    def __init__(self, desk_id, modified, state, cards):
        self.desk_id = desk_id
        self.modified = modified
        self.state = state
        self.cards = cards

    def __repr__(self):
        return '<GameDesk %r>' % self.desk_id


class PlayerEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    card = db.Column(db.String)

    desk_id = db.Column(db.String, db.ForeignKey('game_desk_entity.desk_id'))
    desk = db.relationship('GameDeskEntity', backref=db.backref('players', lazy='dynamic'))

    def __init__(self, desk_id, name, card=None):
        self.desk_id = desk_id
        self.name = name
        self.card = card

    def __repr__(self):
        return '<Player %r/%r>' % self.desk_id, self.username
