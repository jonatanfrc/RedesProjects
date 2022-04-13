import socket

class Client:

    def __init__(self, tcp_port, tcp_ip, buf_size):

        self.tcp_port = tcp_port
        self.tcp_ip = tcp_ip
        self.buf_size = buf_size
        self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def getTcp_ip(self):
        return self.tcp_ip

    def getTcp_port(self):
        return self.tcp_port
    
    def getBuf_size(self):
        return self.buf_size

    def connectSocket(self):

        tcp_ip = self.getTcp_ip()
        tcp_port = self.getTcp_port()
        buf_size = self.getBuf_size()
        tcp_socket = self.tcp_socket

        print("[INFO] Conectando socket com a porta: ",tcp_port)
        tcp_socket.connect((tcp_ip,tcp_port))
        print("[INFO] Socket conectado à porta: ",tcp_port)

        msg = "11101001110"
        msg = msg.encode('utf-8')

        print("[INFO] Enviando dados para o servidor...")
        tcp_socket.send(msg)
        print("[INFO] Dados enviados com sucesso!")

        print("[INFO] Recebendo dados do servidor...")
        data = tcp_socket.recv(buf_size)

        print("[INFO] Decodificando dados recebidos...")
        data = data.decode('utf-8')

        print('[INFO] Dados recbidos do servidor:',data)

        print("[INFO] Desconectando socket...")
        tcp_socket.close()
        print("[INFO] Socket desconectado com sucesso!")

tcp_ip = '127.0.0.1'
buf_size = 30

client = Client(8000, tcp_ip, buf_size)
client.connectSocket()

