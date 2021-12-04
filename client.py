import socket
import json
import protocols as p


c_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_s.connect(("127.0.0.1", 7129))
exit = False
#usualmente en este punto le enviamos un mensaje al servidor para decirle
#que estamos aquí e iniciar la conversación
while not exit:
    try:
        #en este cliente se espera a que el servidor diga algo
        server_msg = json.loads(c_s.recv(1024).decode())
        """if server_msg["protocol"] == p.whatever_protocol:
                manage_this_msg()
        """
    except ConnectionResetError:
        exit = True
        print("El servidor ha sido cerrado")
c_s.close()