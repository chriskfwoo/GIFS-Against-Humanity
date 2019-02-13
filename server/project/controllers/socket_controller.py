from project import socketio


def broadcast_status(room, room_info, scoreboard_info=None):
    socketio.emit('status', {'msg': room_info, 'scoreboard': scoreboard_info}, room=room)


def broadcast_winner(room, winner, scoreboard_info, gif):
    socketio.emit('notify-winner', {'msg': winner, 'scoreboard': scoreboard_info, 'winGif': gif}, room=room)
