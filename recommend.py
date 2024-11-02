import zmq
import random

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def parse_data(data):
    songs = []
    for line in data.strip().split('\n'):
        components = line.split('*')
        if len(components) == 5:
            song = {"ID": components[0], "Title": components[1], "Artist": components[2], "Album": components[3], "Genre": components[4]}
            songs.append(song)
    return songs

def random_num(data_len):
    rand_num = random.randint(0, data_len - 1)
    return rand_num

def find_random_song(data, rand_num):
    rand_song = data[rand_num]
    result = "\n".join(f"{key}: {value}" for key, value in rand_song.items())
    return result



while True:
    message = socket.recv_string()
    print(f"Received song data")
    data = parse_data(message)
    data_len = len(data)
    rand_num = random_num(data_len)
    rand_song = find_random_song(data, rand_num)
    socket.send_string(rand_song)
