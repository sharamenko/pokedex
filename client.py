import socket
import json
import sys
import protocols as p


def manage_server_message(msg):
    print(msg)


def manage_server_menu(m):
    print(m)
    try:
        pokemon = input()
        try:
            p_id = int(pokemon)
            msg_pokemon_id = p.craft_send_pokemon_id(p_id)
            p.send_one_message(c_s, msg_pokemon_id)
        except ValueError:
            p_name = pokemon
            msg_pokemon_name = p.craft_send_pokemon_name(p_name)
            p.send_one_message(c_s, msg_pokemon_name)
    except KeyboardInterrupt:
        print("\nDisconnecting...")
        msg_disconnection = p.craft_send_client_disconnection(c_s.getsockname())
        p.send_one_message(c_s, msg_disconnection)
        sys.exit(0)


def manage_sent_pokemon_info(p_id, p_name, p_type, p_weaknesses):
    print("\n---------------RESULTS---------------\n")
    print(f"{p_name} (N.º{p_id}): Is a {p_type} pokemon who is weak against {p_weaknesses}\n")


c_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_s.connect(("127.0.0.1", 7129))
msg_join = p.craft_join()
p.send_one_message(c_s, msg_join)
end = False
while not end:
    try:
        server_msg = json.loads((p.recv_one_message(c_s)).decode())
        if server_msg["Protocol"] == p.PROTOCOL_SERVER_MESSAGE:
            message = server_msg["Message"]
            manage_server_message(message)
        elif server_msg["Protocol"] == p.PROTOCOL_SERVER_MENU:
            menu = server_msg["Menu"]
            manage_server_menu(menu)
        elif server_msg["Protocol"] == p.PROTOCOL_SEND_POKEMON_INFO:
            pokemon_num = server_msg["Pokemon_num"]
            pokemon_name = server_msg["Pokemon_name"]
            pokemon_type = server_msg["Pokemon_type"]
            pokemon_weaknesses = server_msg["Pokemon_weaknesses"]
            manage_sent_pokemon_info(pokemon_num, pokemon_name, pokemon_type, pokemon_weaknesses)
    except ConnectionResetError:
        end = True
        print("Server is closed.")
    except AttributeError:
        pass
c_s.close()
