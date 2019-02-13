SCOREBOARD = {}


def get_scoreboard(room):
    global SCOREBOARD

    if room not in SCOREBOARD:
        SCOREBOARD[room] = {}
    return SCOREBOARD[room]


def update_scoreboard(room, winner):
    global SCOREBOARD

    if room not in SCOREBOARD:
        SCOREBOARD[room] = {}
    if winner not in SCOREBOARD[room]:
        SCOREBOARD[room].update({winner: 1})
    else:
        SCOREBOARD[room][winner] = SCOREBOARD[room][winner] + 1
    return SCOREBOARD[room]
