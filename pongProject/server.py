import socket
from _thread import *
from player import Player
import pickle

server = "localhost"
port = 5555

# create socket in TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # try connect the socket to the server & port
    s.bind((server, port))
except socket.error as e:
    str(e)

# Listening to possible connections, 2 can wait in line to enter
s.listen(2)
print("Waiting for a connection, Server Started")

# create list with the players
players = [Player(0, 200, 15, 130, (255, 255, 255)), Player(486, 200, 15, 130, (255, 255, 255))]


def threaded_client(conn, player):
    # sending starting player object
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                # print("Received: ", data)
                # print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    # accepting connection
    conn, addr = s.accept()
    print("Connected to:", addr)
    players[currentPlayer].ready = True
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
