import socket

class Server:

    def __init__(self, tcp_port, tcp_ip, buf_size, datamsg):

        self.tcp_port = tcp_port
        self.tcp_ip = tcp_ip
        self.buf_size = buf_size
        self.datamsg = datamsg
        self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def getTcp_ip(self):
        return self.tcp_ip

    def getTcp_port(self):
        return self.tcp_port
    
    def getBuf_size(self):
        return self.buf_size

    def createSocket(self):

        tcp_ip = self.getTcp_ip()
        tcp_port = self.getTcp_port()
        
        print("[INFO] Socket criado!")

        self.tcp_socket.bind((tcp_ip,tcp_port))
        print("[INFO] Socket está ligado à porta:",tcp_port)

        self.tcp_socket.listen(1)
        print("[INFO] Socket está escutando")

    def recieve(self):

        # Estimula o erro em transmissão mudando um valor de bit
        # 10101001110 -> 11101001110, erro na décima posição.
        def calculateRedundantBits(m):

            for i in range(m):
                if(2**i >= m + i + 1):
                    return i

        def positionRedundantBits(data, redundant):

            j = 0
            k = 1
            m = len(data)
            result = ''

            for i in range(1, m + redundant +1):
                if(i == 2**j):
                    result = result + '0'
                    j += 1
                else:
                    result = result + data[-1 * k]
                    k += 1
            return result[::-1]

        def calculateParityBits(arr, redundant):

            n = len(arr)

            for i in range(redundant):
                value = 0
                for j in range(1, n + 1):
                    if(j & (2**i) == (2**i)):
                        value = value ^ int(arr[-1 * j])

                arr = arr[:n-(2**i)] + str(value) + arr[n-(2**i)+1:]
            return arr

        def findError(arr, nr):

            n = len(arr)
            res = 0

            for i in range(nr):
                value = 0
                for j in range(1, n + 1):
                    if(j & (2**i) == (2**i)):
                        value = value ^ int(arr[-1 * j])

                res = res + value*(10**i)

            return int(str(res), 2)

        size = len(self.datamsg)
        redundant = calculateRedundantBits(size)

        arr = positionRedundantBits(self.datamsg, redundant)

        arr = calculateParityBits(arr, redundant)

        print("[INFO] Dados a serem transferidos são: " + arr)

        tcp_socket = self.tcp_socket
        client, address = tcp_socket.accept()
        buf_size = self.getBuf_size()

        print("[INFO] Endereço de conexão vindo de:",address)

        print("[INFO] Recebendo dados do cliente...")
        data = client.recv(buf_size)

        print("[INFO] Decodificando dados do cliente...")
        data = data.decode('utf-8')

        print("[INFO] Dados recebidos do cliente:",data)

        if(str(data) == arr):

            msg = "Dados corretos"
            msg = msg.encode('utf-8')

            print("[INFO] Enviando dados para o cliente...")
            client.send(msg)
            print("[INFO] Dados enviados com sucesso")

        else:

            print("[INFO] Erro encontrado, enviando mensagem de erro")
            correction = findError(str(data), redundant)
            response1 = "Erro encontrado. Posição: " + str(correction)
            response1 = response1.encode('utf-8')
            client.send(response1)
            print("[INFO] Desconectando o client...")
            client.close()

            print("[INFO] Desconectando socket...")
            tcp_socket.close()
            print("[INFO] Socket desconectado!")

tcp_ip = '127.0.0.1'
buf_size = 30

server = Server(8000, tcp_ip, buf_size, '1011001')
server.createSocket()
server.recieve()
