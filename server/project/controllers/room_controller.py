import random
import string

from project.externals.giphy import giphy_api


UNIQUE_ROOMS = []
ROOMS_STORE = {}


def create_unique_room_id():
    global UNIQUE_ROOMS

    while True:
        N = 4
        id = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=N))
        if id not in UNIQUE_ROOMS:
            UNIQUE_ROOMS.append(id)
            return id


def is_user_in_room(room, user):
    global ROOMS_STORE

    if room not in ROOMS_STORE:
        return False
    if user not in ROOMS_STORE[room]['listOfUsers']:
        return False
    return True


def join_game_room(room, user):
    global ROOMS_STORE

    if room not in ROOMS_STORE:
        create_room(room, user)

    if user not in ROOMS_STORE[room]['listOfUsers']:
        ROOMS_STORE[room]["listOfUsers"].append(user)
        ROOMS_STORE[room]["userNotJudge"].append(user)

    return ROOMS_STORE[room]


def leave_game_room(room, user):
    global ROOMS_STORE

    if room in ROOMS_STORE and user in ROOMS_STORE[room]['listOfUsers']:
        ROOMS_STORE[room]["listOfUsers"].remove(user)
        if user in ROOMS_STORE[room]["userNotJudge"]:
            ROOMS_STORE[room]["userNotJudge"].remove(user)

    return ROOMS_STORE[room]


def start_game_room(room):
    global ROOMS_STORE

    ROOMS_STORE[room]['started'] = True
    return new_round(room)


def new_round(room):
    import project as gifs
    questions = gifs.QUESTIONS
    r = random.randint(1, 193)

    # new judge
    ROOMS_STORE[room]['question'] = questions[r]
    ROOMS_STORE[room]['judge'] = room_user_turns(room)
    ROOMS_STORE[room]['gifPicks'] = {}

    return ROOMS_STORE[room]


def room_user_turns(room):
    global ROOMS_STORE

    if len(ROOMS_STORE[room]['userNotJudge']) == 0:
        ROOMS_STORE[room]['userNotJudge'] = ROOMS_STORE[room]['userWasJudge']
    user_to_judge = ROOMS_STORE[room]['userNotJudge'].pop(0)

    ROOMS_STORE[room]['userWasJudge'].append(user_to_judge)
    return user_to_judge


def user_select_gif(room, user, gif):
    global ROOMS_STORE

    ROOMS_STORE[room]['gifPicks'][user] = gif
    return ROOMS_STORE[room]


def user_new_hand(room, used_gif):
    global ROOMS_STORE

    available_gifs = ROOMS_STORE[room]['availableGifs']
    id, url = available_gifs.popitem()
    new_gif = {'id': id, 'gif': url}
    ROOMS_STORE[room]['usedGifs'].append(new_gif)

    return new_gif


def create_room(room, user):
    global ROOMS_STORE

    gifs_available = giphy_api()

    ROOMS_STORE[room] = {
        'question': '',
        'captain': user,
        'listOfUsers': [],
        'started': False,
        'judge': '',
        'availableGifs': gifs_available,
        'usedGifs': [],
        'round': 0,
        'userNotJudge': [],
        'userWasJudge': [],
        'gifPicks': {}
    }
