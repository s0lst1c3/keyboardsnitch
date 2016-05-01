from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
socketio = SocketIO(app)

@app.route('/')
def index():

    return render_template('index.html')

if __name__ == '__main__':

    socketio.run(app)
