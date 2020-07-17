from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from queue import SimpleQueue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player_1 = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
reverse_direction = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
traversal_path = []

current_map = {}
prev_room = None

def find_nearest_unexplored(room_id, current_map):
    """
    Breadth-first search for nearest '?' exit to room.
    """
    searched = {}
    to_search = SimpleQueue()
    to_search.put((room_id, None))
    while to_search.qsize() > 0:
        (room, previous_direction) = to_search.get()
        if room not in searched:
            searched[room] = previous_direction
            options = []
            for exit_dir, next_room in current_map[room].items():
                if next_room == '?':
                    options.append(exit_dir)
            if len(options) > 0:
                path = [random.choice(options)]
                step = previous_direction
                while step is not None:
                    path.append(step)
                    room = current_map[room][reverse_direction[step]]
                    step = searched[room]
                return path[::-1]

            for exit_dir, neighboring_room in current_map[room].items():
                if neighboring_room != '?' and \
                    neighboring_room not in searched:
                    to_search.put((neighboring_room, exit_dir))

def get_next_move(player, current_map):
    """
    Return next move or series of moves, given present location and map.
    """
    options = []
    for exit_dir, room in current_map[player.current_room.id].items():
        if room == '?':
            options.append(exit_dir)
    if len(options) > 0:
        return [random.choice(options)]
    if map_complete(current_map):
        return None
    return find_nearest_unexplored(player.current_room.id, current_map)

def map_complete(current_map):
    return not any(['?' in exits.values() for exits in current_map.values()])

def add_new_room(room, prev_room, prev_dir, current_map):
    # Add previously unexplored room to map
    current_map[room.id] = {direction: '?' for direction in room.get_exits()}
    current_map[room.id][reverse_direction[last_dir]] = last_room
    current_map[last_room][last_dir] = room.id


# Seed map with starting room.
current_map[player_1.current_room.id] = {direction: '?' for direction in \
                                       player_1.current_room.get_exits()}

next_move = get_next_move(player_1, current_map)
while next_move is not None:
    traversal_path += next_move
    for direction in next_move:
        prev_room = player_1.current_room.id
        player_1.travel(direction)

    if player_1.current_room.id not in current_map:
        add_new_room(player_1.current_room,
                     prev_room,
                     traversal_path[-1],
                     current_map)
    else:
        current_map[prev_room][traversal_path[-1]] = player_1.current_room.id
        current_map[player_1.current_room.id][reverse_direction[traversal_path[-1]]] = \
            prev_room
    next_move = get_next_move(player_1, current_map)



# TRAVERSAL TEST
visited_rooms = set()
player_1.current_room = world.starting_room
visited_rooms.add(player_1.current_room)

for move in traversal_path:
    player_1.travel(move)
    visited_rooms.add(player_1.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
