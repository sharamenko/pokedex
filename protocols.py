import struct
import json
import sys

PROTOCOL_JOIN = "Join"
PROTOCOL_SERVER_MESSAGE = "Server_Message"
PROTOCOL_SERVER_MENU = "Server_Menu"
PROTOCOL_SEND_POKEMON_ID = "Send_Pokemon_ID"
PROTOCOL_SEND_POKEMON_NAME = "Send_Pokemon_Name"
PROTOCOL_SEND_POKEMON_INFO = "Send_Pokemon_Info"
PROTOCOL_SEND_CLIENT_DISCONNECTION = "Send_Client_Disconnection"


def craft_join():
    msg = {"Protocol": PROTOCOL_JOIN}
    return json.dumps(msg).encode()


def craft_server_message(message):
    msg = {"Protocol": PROTOCOL_SERVER_MESSAGE, "Message": message}
    return json.dumps(msg).encode()


def craft_server_menu(menu):
    msg = {"Protocol": PROTOCOL_SERVER_MENU, "Menu": menu}
    return json.dumps(msg).encode()


def craft_send_pokemon_id(pokemon_id):
    msg = {"Protocol": PROTOCOL_SEND_POKEMON_ID, "ID": pokemon_id}
    return json.dumps(msg).encode()


def craft_send_pokemon_name(pokemon_name):
    msg = {"Protocol": PROTOCOL_SEND_POKEMON_NAME, "Name": pokemon_name}
    return json.dumps(msg).encode()


def craft_send_pokemon_info(num, name, p_type, weaknesses):
    msg = {"Protocol": PROTOCOL_SEND_POKEMON_INFO, "Pokemon_num": num, "Pokemon_name": name,
           "Pokemon_type": p_type, "Pokemon_weaknesses": weaknesses}
    return json.dumps(msg).encode()


def craft_send_client_disconnection(c_disconnected):
    msg = {"Protocol": PROTOCOL_SEND_CLIENT_DISCONNECTION, "Client_disconnected": c_disconnected}
    return json.dumps(msg).encode()


def recvall(sock, count):
    try:
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf
    except KeyboardInterrupt:
        pass
    except OSError:
        pass


def send_one_message(sock, data):
    try:
        length = len(data)
        sock.sendall(struct.pack('!I', length))
        sock.sendall(data)
    except BrokenPipeError:
        print("You tried sending a message to a closed server. Exiting...")
        sys.exit(1)


def recv_one_message(sock):
    try:
        lengthbuf = recvall(sock, 4)
        length, = struct.unpack('!I', lengthbuf)
        return recvall(sock, length)
    except TypeError:
        pass
