from random import choice
import time

from flask_restful import Resource, abort, reqparse

from ScrumPokerTablePy import db, events
from ScrumPokerTablePy.models import GameDeskEntity, PlayerEntity, GameDeskStateEnum, GameDeskHistoryEntity


def return_desk(desk):
    players = [dict(name=p.name, card=p.card) for p in desk.players.all()]
    return dict(desk_id=desk.desk_id, state=desk.state, modified=desk.modified, players=players, cards=desk.cards)


def get_desk(desk_id):
    desk = GameDeskEntity.query.get(desk_id)
    if not desk:
        abort(404)
    return desk


def get_desk_history_list(desk_id):
    return GameDeskHistoryEntity.query \
        .filter_by(desk_id=desk_id) \
        .order_by(GameDeskHistoryEntity.modified) \
        .all()


def store_desk_history(desk):
    players = desk.players.all()
    if all([p.card is None for p in players]):
        return

    content = [dict(name=x.name, card=x.card) for x in desk.players]
    desk_history = GameDeskHistoryEntity(desk.desk_id, desk.modified, content)
    db.session.add(desk_history)
    db.session.commit()


def return_desk_history(desk_history_list):
    return [dict(modified=h.modified, state=h.content) for h in desk_history_list]


class GameDeskFinish(Resource):
    def post(self, desk_id):
        desk = get_desk(desk_id)
        desk.state = GameDeskStateEnum.Display
        desk.modified = time.time()
        db.session.commit()
        store_desk_history(desk)
        events.send(desk_id)
        return '', 200


class GameDeskStart(Resource):
    def post(self, desk_id):
        desk = get_desk(desk_id)
        desk.state = GameDeskStateEnum.Voting
        desk.modified = time.time()
        for p in desk.players.all():
            p.card = None
        db.session.commit()
        events.send(desk_id)
        return '', 200


class GameDesk(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('X-Polling-Timeout', type=int, location='headers', dest='timeout')
        self.parser.add_argument('X-Modified', type=float, location='headers', dest='modified')

    def get(self, desk_id):
        args = self.parser.parse_args()
        modified = args['modified']
        timeout = args['timeout']
        desk = get_desk(desk_id)

        if desk.modified == modified:
            if not events.receive(desk_id, timeout):
                return '', 304

        return return_desk(desk)

    @staticmethod
    def delete(desk_id):
        desk = get_desk(desk_id)
        db.session.delete(desk)
        GameDeskHistoryEntity.query.filter_by(desk_id=desk_id).delete()
        db.session.commit()
        events.send(desk_id)
        return '', 200


class GameDeskHistory(Resource):
    def get(self, desk_id):
        return return_desk_history(get_desk_history_list(desk_id))


class GameDeskList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('cards', type=list, required=True, location='json')

    @staticmethod
    def get():
        return [return_desk(d) for d in GameDeskEntity.query.all()]

    def post(self):
        args = self.parser.parse_args()
        desk_cards = args['cards']

        desk_id = None
        while True:
            desk_id = ''.join(choice('ABCDEFGHJKLMNPQRSTUVWXYZ123456789') for _ in range(8)).lower()
            if not GameDeskEntity.query.get(desk_id):
                break

        desk = GameDeskEntity(desk_id, time.time(), GameDeskStateEnum.Waiting, desk_cards)
        db.session.add(desk)
        db.session.commit()
        return return_desk(desk)


class Player(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('card')

    def post(self, desk_id, player_name):
        player_name = self.get_sanitized_player_name(player_name)
        desk = get_desk(desk_id)

        self.create_player(desk, player_name)
        events.send(desk_id)
        return '', 200

    def put(self, desk_id, player_name):
        player_name = self.get_sanitized_player_name(player_name)
        desk = get_desk(desk_id)

        if desk.state == GameDeskStateEnum.Display:
            abort(406)

        args = self.parser.parse_args()
        card = args['card']

        self.pre_update_trigger(desk, card)
        self.update_player(desk, player_name, card)
        self.post_update_trigger(desk)
        events.send(desk_id)
        return '', 200

    @staticmethod
    def get_sanitized_player_name(player_name):
        player_name = player_name.strip().lower() if player_name is not None else player_name
        if player_name is None:
            abort(400)
        return player_name

    @staticmethod
    def create_player(desk, player_name):
        player = desk.players.filter_by(name=player_name).first()
        if not player:
            player = PlayerEntity(desk.desk_id, player_name, None)
            db.session.add(player)
            desk.modified = time.time()
            db.session.commit()

    @staticmethod
    def update_player(desk, player_name, card):
        player = desk.players.filter_by(name=player_name).first()
        if not player:
            abort(404)
        player.card = card
        desk.modified = time.time()
        db.session.commit()

    @staticmethod
    def pre_update_trigger(desk, card):
        if desk.state != GameDeskStateEnum.Voting and card:
            players = desk.players.all()
            if len(players) > 1:
                desk.state = GameDeskStateEnum.Voting
                for p in desk.players.all():
                    p.card = None
                desk.modified = time.time()
                db.session.commit()

    @staticmethod
    def post_update_trigger(desk):
        players = desk.players.all()
        if desk.state == GameDeskStateEnum.Voting and all([p.card is not None for p in players]):
            desk.state = GameDeskStateEnum.Display
            desk.modified = time.time()
            db.session.commit()
            store_desk_history(desk)
