from flask import Blueprint, jsonify, request
from project.controllers.room_controller import create_unique_room_id, join_game_room, \
    is_user_in_room, user_select_gif, user_new_hand
from project.controllers.scoreboard_controller import get_scoreboard
from project.controllers.socket_controller import broadcast_status
from project.utils.logger import logger

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/room/create', methods=["GET"])
def get_room():
    id = create_unique_room_id()
    return jsonify({'room': id, 'error': ''})


@api_bp.route('/room/join', methods=["POST"])
def join_room():
    try:
        response = request.json
        room = response['room'].upper()
        user = response['user']

        if is_user_in_room(room, user):
            return jsonify({'error': 'user already exist', 'gifs': []})

        room_info = join_game_room(room, user)
        available_gifs = room_info['availableGifs']
        list_gifs = []
        for i in range(5):
            id, url = available_gifs.popitem()
            gif_dict = {'id': id, 'gif': url}
            list_gifs.append(gif_dict)
            room_info['usedGifs'].append(gif_dict)
        return jsonify({'error': '', 'gifs': list_gifs})
    except Exception as msg:
        logger.exception(msg)
        return jsonify({'error': 'cannot post', 'selectedGif': ''})


@api_bp.route('/room/select', methods=["POST"])
def user_select():
    try:
        response = request.json
        room = response['room'].upper()
        user = response['user']
        gif = response['gif']
        room_info = user_select_gif(room, user, gif)
        scoreboard_info = get_scoreboard(room)
        broadcast_status(room, room_info, scoreboard_info)
        return jsonify({'error': '', 'selectedGif': gif})
    except Exception as msg:
        logger.exception(msg)
        return jsonify({'error': 'cannot post', 'selectedGif': ''})


@api_bp.route('/room/hand/new', methods=["POST"])
def new_gif():
    try:
        response = request.json
        room = response['room'].upper()
        gif_dict = response['gif']

        if len(gif_dict.keys()) == 0:
            return jsonify({'error': '', 'newGif': ''})

        new_gif = user_new_hand(room, gif_dict)
        return jsonify({'error': '', 'newGif': new_gif})
    except Exception as msg:
        logger.exception(msg)
        return jsonify({'error': 'cannot post', 'newGif': ''})
