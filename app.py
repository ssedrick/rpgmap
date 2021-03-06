import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__)
socketio = SocketIO(app)
ROOMS = {}


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('create')
def on_create(data):
    pass


@socketio.on('createRoom')
def handle_create(data):
    print('create room')
    if data['code'] not in ROOMS:
        if data['role'] == 'ADMIN':
            print('setting up room', data['state'])
            ROOMS[data['code']] = data['state']
        join_room(data['code'])
        emit('createdRoom', {'room': data['code']})

@socketio.on('joinRoom')
def handle_join(data):
    print('join room')
    if data['code'] in ROOMS:
        join_room(data['code'])
        emit('joinedRoom', {'code': data['code'], 'state': ROOMS[data['code']], 'name': data['role']}, room=data['code'])


@socketio.on('sendState')
def handle_state(data):
    print('handling state', data['state'])
    if data['code'] in ROOMS:
        ROOMS[data['code']] = data['state']
        state = data['state']
        state['map'].pop('role')
        emit('message', { 'code': data['code'], 'state': state }, room=data['code'])



if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info('running app')
    socketio.run(app, debug=True, log_output=True)
