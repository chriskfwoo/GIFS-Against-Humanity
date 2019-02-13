from flask_socketio import join_room, leave_room
from project import socketio
from project.controllers.room_controller import join_game_room, leave_game_room, start_game_room, new_round
from project.controllers.scoreboard_controller import get_scoreboard, update_scoreboard
from project.controllers.socket_controller import broadcast_status, broadcast_winner
from project.utils.logger import logger


@socketio.on('join', namespace='/')
def on_join(data):
    room = data['room'].upper()
    user = data['user']

    room_info = join_game_room(room, user)
    join_room(room)
    scoreboard_info = get_scoreboard(room)
    broadcast_status(room, room_info, scoreboard_info)
    logger.info(f'(JOINED): {user} --> joined room {room}.')


@socketio.on('leave', namespace='/')
def on_leave(data):
    room = data['room'].upper()
    user = data['user']

    room_info = leave_game_room(room, user)
    leave_room(data['room'])
    scoreboard_info = get_scoreboard(room)
    broadcast_status(room, room_info, scoreboard_info)
    logger.info(f'(LEAVE): {user} --> left room {room}.')


@socketio.on('start', namespace='/')
def start_game(data):
    room = data['room'].upper()

    room_info = start_game_room(room)
    scoreboard_info = get_scoreboard(room)
    broadcast_status(room, room_info, scoreboard_info)
    logger.info(f'(START): room {room} has started.')


@socketio.on('winner', namespace='/')
def winner_game(data):
    room = data['room'].upper()
    winner = data['winner']
    gif = data['gif']

    scoreboard_info = update_scoreboard(room, winner)
    broadcast_winner(room, winner, scoreboard_info, gif)
    room_info = new_round(room)
    broadcast_status(room, room_info, scoreboard_info)
    logger.info(f'(WINNER): {winner} won in room {room}.')
