from flask import session
from flask_socketio import SocketIO, emit, join_room, leave_room
from . import db
import datetime

socketio = SocketIO()

@socketio.on('joined', namespace='/chat')
def joined(message):
    ''' Sent by clients when they enter a room.
     A status message is broadcast to all people in the room. '''
    session['chat_room'] = message['room']
    session['chat_type'] = message['type']
    room = session.get('chat_room', '')
    join_room(room)
    emit('status', {'msg': session.get('user_name', '') + ' has entered the room.'}, room=room)
    if message['type'] != 'friend':
        db.Chat.insert_one({
            'room': room,
            'msg': session.get('user_name', '') + ' has entered the room.',
            'sent_at': datetime.datetime.now()
        })
        emit('status', {'msg': session.get('user_name', '') + ' has entered the room.'}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    ''' Sent by a client when the user entered a new message.
    The message is sent to all people in the room. '''
    room = session.get('chat_room', '')
    chat_type = session.get('chat_type', '')
    if room != '' and chat_type != 'friend':
        db.Chat.insert_one({
            'room': room,
            'msg': session.get('user_name', '') + ': ' + message['msg'],
            'sent_at': datetime.datetime.now()
        })
    emit('message', {'msg': session.get('user_name', '') + ': ' + message['msg']}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    ''' Sent by clients when they leave a room.
    A status message is broadcast to all people in the room. '''
    room = session.get('chat_room', '')
    if room != '':
        leave_room(room)
        db.Chat.insert_one({
            'room': room,
            'msg': session.get('user_name', '') + ' has left the room.',
            'sent_at': datetime.datetime.now()
        })
    emit('status', {'msg': session.get('user_name', '') + ' has left the room.'}, room=room)
