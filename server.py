import socket
import threading
import json
import protocols as p
import pokedex


pokedex = pokedex.Pokedex()
client_threads_running = []


def manage_join(c_s):
    menu = p.craft_server_menu("Use Ctrl + C to exit the program. \n"
                               "Search a pokemon by name or using its National Pokedex Number: ")
    p.send_one_message(c_s, menu)


def format_pokemon_weaknesses(list_weaknesses):
    if len(list_weaknesses) <= 2:
        str_weaknesses = ' and '.join(list_weaknesses)
    else:
        str_weaknesses = ', '.join(list_weaknesses[0:(len(list_weaknesses) - 1)])
        str_weaknesses += " and " + list_weaknesses[len(list_weaknesses) - 1]
    return str_weaknesses


def manage_sent_pokemon_id(c_s, sent_id):
    global pokedex
    pokemon = ""
    pokemon_id = 0
    str_pokemon_type = ""
    str_pokemon_weaknesses = ""
    if 1 <= sent_id <= len(pokedex.list_pokemons):
        for pkmn in pokedex.list_pokemons:
            if pkmn.get_id_num() == sent_id:
                pokemon_id = pkmn.get_id_num()
                pokemon = pkmn.get_name()
                pokemon_type = pkmn.get_pkmn_type()
                pokemon_weaknesses = pkmn.get_weaknesses()
                str_pokemon_type = ' and '.join(pokemon_type)
                str_pokemon_weaknesses = format_pokemon_weaknesses(pokemon_weaknesses)
                break
        msg_info = p.craft_send_pokemon_info(pokemon_id, pokemon, str_pokemon_type, str_pokemon_weaknesses)
        p.send_one_message(c_s, msg_info)
        manage_join(c_s)
    else:
        msg_error = p.craft_server_message("National Pokedex Number must be between 1-151.")
        p.send_one_message(c_s, msg_error)
        manage_join(c_s)


def manage_sent_pkmn_name(c_s, sent_name):
    global pokedex
    found = False
    pokemon = ""
    pokemon_id = 0
    str_pokemon_type = ""
    str_pokemon_weaknesses = ""
    for pkmn in pokedex.list_pokemons:
        if pkmn.get_name().lower() == sent_name.lower():
            found = True
            pokemon_id = pkmn.get_id_num()
            pokemon = pkmn.get_name()
            pokemon_type = pkmn.get_pkmn_type()
            pokemon_weaknesses = pkmn.get_weaknesses()
            str_pokemon_type = ' and '.join(pokemon_type)
            str_pokemon_weaknesses = format_pokemon_weaknesses(pokemon_weaknesses)
            break
    if found:
        msg_info = p.craft_send_pokemon_info(pokemon_id, pokemon, str_pokemon_type, str_pokemon_weaknesses)
        p.send_one_message(c_s, msg_info)
        manage_join(c_s)
    else:
        msg_error = p.craft_server_message("No pokemon matched your search!")
        p.send_one_message(c_s, msg_error)
        manage_join(c_s)


def manage_client_disconnection(c_disconnected):
    global client_threads_running
    ServerThread.close_client_disconnected(c_disconnected)


class ClientThread(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.c_s = client_socket
        self.client_exit = False

    def set_disconnected(self):
        self.client_exit = True

    def run(self):
        while not self.client_exit:
            try:
                message = json.loads(p.recv_one_message(self.c_s).decode())
                if message["Protocol"] == p.PROTOCOL_JOIN:
                    manage_join(self.c_s)
                elif message["Protocol"] == p.PROTOCOL_SEND_POKEMON_ID:
                    sent_id = message["ID"]
                    manage_sent_pokemon_id(self.c_s, sent_id)
                elif message["Protocol"] == p.PROTOCOL_SEND_POKEMON_NAME:
                    sent_name = message["Name"]
                    manage_sent_pkmn_name(self.c_s, sent_name)
                elif message["Protocol"] == p.PROTOCOL_SEND_CLIENT_DISCONNECTION:
                    client_disconnected = message["Client_disconnected"]
                    manage_client_disconnection(client_disconnected)
            except ConnectionResetError:
                self.set_disconnected()
            except ConnectionAbortedError:
                self.set_disconnected()
            except AttributeError:
                pass


class ServerThread(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.stop = False
        self.s_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_s.bind((ip, port))
        self.s_s.listen(10)

    def set_stop(self):
        self.stop = False

    @staticmethod
    def close_client_connections():
        global client_threads_running
        for thread in client_threads_running:
            thread.c_s.close()

    @staticmethod
    def close_client_disconnected(c_disconnected):
        global client_threads_running
        tuple_c_disconnected = tuple(c_disconnected)
        for client_thread in client_threads_running:
            if client_thread.c_s.getpeername() == tuple_c_disconnected:
                print(f"Client in {client_thread.c_s.getpeername()} disconnected...")
                client_thread.set_stop()

    def run(self):
        global client_threads_running
        while not self.stop:
            try:
                c_s, c_a = self.s_s.accept()
                client_thread = ClientThread(c_s)
                print(f"Client from: {c_a}")
                client_thread.daemon = True
                client_thread.start()
                client_threads_running.append(client_thread)
            except OSError:
                self.stop = True
                ServerThread.close_client_connections()
            except KeyboardInterrupt:
                self.stop = True
                ServerThread.close_client_connections()
        print("Exiting server...")


server_thread = ServerThread("0.0.0.0", 7129)
server_thread.daemon = True
server_thread.start()

end = False
while not end:
    server_input = input("Enter exit to close server: \n")
    if server_input == "exit":
        try:
            end = True
            server_thread.close_client_connections()
            server_thread.s_s.close()
        except OSError:
            print("Server closed.")
        except ConnectionAbortedError:
            print("Closed connection.")
        except ConnectionResetError:
            print("Closed connection.")
