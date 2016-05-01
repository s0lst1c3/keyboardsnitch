from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit


def


if __name__ == '__main__':

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    socketio = SocketIO(app)

