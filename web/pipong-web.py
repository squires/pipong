import json
import time

from gevent import monkey
monkey.patch_all()

from flask import Flask, app, render_template
from werkzeug.debug import DebuggedApplication

from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

flask_app = Flask(__name__)
flask_app.debug = True

scores = {
    'red': 0,
    'blue': 0
}

serve_order = ['red', 'blue']

reset_score_flag = False
reset_score_timestamp = 0

def clear_reset_score_flag():
    global reset_score_flag
    reset_score_flag = False

def init_reset_timestamp():
    reset_score_timestamp = time.time();

def get_serve():
    total_scores = scores['red'] + scores['blue']
    serve_idx = (total_scores // 2) % 2
    return serve_order[serve_idx]

def get_score_msg():
    return json.dumps({'msg_type': 'scores', 'scores': scores, 'serve': get_serve()});

def rotate_serve():
    tmp = serve_order[0]
    serve_order[0] = serve_order[1]
    serve_order[1] = tmp

class PingPong(WebSocketApplication):
    sockets = {}

    def on_open(self):
        self.sockets[id(self.ws)] = self.ws
        self.ws.send(get_score_msg())
        print 'websocket client connected (%d connected)' % len(self.sockets.keys())

    def on_close(self, reason):
        if id(self.ws) in self.sockets:
            del self.sockets[id(self.ws)]
        print 'websocket connection closed (%d connected)' % len(self.sockets.keys())

    def on_message(self, message):
        if message is None:
            return

        #if message['msg_type'] == 'refresh':
        #    return

    @classmethod
    def broadcast(cls, message):
        for ws in cls.sockets.values():
            ws.send(message)

        #for client in self.ws.handler.server.clients.values():
        #    client.ws.send(json.dumps({
        #        'msg_type': 'state'
        #    }))

@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/static/<path:filename>')
def static_file():
    return app.send_from_directory('/home/dev/pingpong-web/static', filename)

@flask_app.route('/score/reset')
def score_reset():
    global reset_score_flag, reset_score_timestamp
    if reset_score_flag:
        if time.time() < (reset_score_timestamp + 1):
            scores['red'] = 0
            scores['blue'] = 0
            rotate_serve()
            PingPong.broadcast(json.dumps({'msg_type': 'reset', 'serve': get_serve()}))
        else:
            reset_score_flag = False
    else:
        reset_score_flag = True
        reset_score_timestamp = time.time()
    return json.dumps({'scores': scores});

@flask_app.route('/score/red/up')
def score_red_up():
    clear_reset_score_flag()
    scores['red'] = scores['red'] + 1
    PingPong.broadcast(get_score_msg())
    return json.dumps({'scores': scores});

@flask_app.route('/score/red/down')
def score_red_down():
    clear_reset_score_flag()
    if scores['red'] > 0:
        scores['red'] = scores['red'] - 1
    PingPong.broadcast(get_score_msg())
    return json.dumps({'scores': scores});

@flask_app.route('/score/blue/up')
def score_blue_up():
    clear_reset_score_flag()
    scores['blue'] = scores['blue'] + 1
    PingPong.broadcast(get_score_msg())
    return json.dumps({'scores': scores});

@flask_app.route('/score/blue/down')
def score_blue_down():
    clear_reset_score_flag()
    if scores['blue'] > 0:
        scores['blue'] = scores['blue'] - 1
    PingPong.broadcast(get_score_msg())
    return json.dumps({'scores': scores});

WebSocketServer(
    ('0.0.0.0', 8000),

    Resource({
        '^/socket': PingPong,
        '^/.*': DebuggedApplication(flask_app)
    }),

    debug = False
).serve_forever()

