import socket
import threading
import json

client_threads_running = []

class ClientThread(threading.Thread):

    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.c_s = client_socket
        self.client_exit = False

    def run(self):
        while not self.client_exit:
            try:
                message = json.loads(self.c_s.recv(1024).decode())
                print("Mensaje recibido", message)
                """if message["protocol"] == p.whatever_protocol:
                    manage_this_msg()"""
            except ConnectionResetError:
                self.client_exit = True
            except ConnectionAbortedError:
                self.client_exit = True


class ServerThread(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.stop = False
        self.s_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_s.bind((ip, port))
        self.s_s.listen(100)

    @staticmethod
    def close_client_connections():
        global client_threads_running
        for th in client_threads_running:
            th.c_s.close()

    def run(self):
        #si queremos que la variable pueda ser modificada desde el hilo tenemos
        #que utilizar la sentencia global
        global client_threads_running
        while not self.stop:
            try:
                c_s, c_a = self.s_s.accept()
                print("Conexión desde", c_a)
                client_thread = ClientThread(c_s)
                client_thread.start()
                #Añadimos el hilo a una lista para poder controlarlo desde el 
                #programa principal
                client_threads_running.append(client_thread)

            except OSError:
                self.stop = True
                ServerThread.close_client_connections()
        print("Sale del servidor")

server_thread = ServerThread("0.0.0.0", 7129)
server_thread.start()

exit = False
while not exit:
    server_input = input("Enter exit to close server")
    if server_input == "exit":
        try:
            exit = True
            server_thread.s_s.close()
        except OSError:
            print("Se ha cerrado el servidor")
        except ConnectionAbortedError:
            print("Conexion cerrada")
        except ConnectionResetError:
            print("Conexión cerrada")
