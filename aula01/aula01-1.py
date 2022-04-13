from typing import List

class Camada:
    
    superior = None
    inferior = None

    @classmethod
    def connect_all(cls, *Camadas : List['Camada']):
        for a, b in zip(Camadas[:-1], Camadas[1:]):
            a.inferior.add_listener(b.superior)
            b.superior.add_listener(a.inferior)

    @classmethod
    def crossover(cls, a : 'Camada', b : 'Camada'):
        a.inferior.add_listener(b.inferior)
        b.inferior.add_listener(a.inferior)

class Listener():

    def next(self, data):
        raise NotImplementedError()

class Interface(Listener): 

    def next(self, data):
        raise NotImplementedError()

    def add_listener(self, listener : Listener):
        raise NotImplementedError()

class BaseLayer(Camada):

    up_stream = None
    down_stream = None

    def __init__(self):
        self.up_stream = []
        self.down_stream = []

        Camada = self

        class InterfSuperior(Interface):
            
            def add_listener(self, listener : Listener):
                Camada.up_stream.append(listener)

            def next(self, data):
                Camada.send(data)


        self.superior = InterfSuperior()

        class InterfInferior(Interface):
            
            def add_listener(self, listener : Listener):
                Camada.down_stream.append(listener)

            def next(self, data):
                Camada.receive(data)

        self.inferior = InterfInferior()

    def fire_up_stream(self,data):
        for listener in self.up_stream:
            listener.next(data)

    def fire_down_stream(self,data):
        for listener in self.down_stream:
            listener.next(data)

class CamadaNormal(BaseLayer):
    def receive(self,data):
        self.fire_up_stream(data)

    def send(self,data):
        self.fire_down_stream(data)

class CamadaInvertida(BaseLayer):

    def receive(self,data):
        self.fire_up_stream(data[::-1])

    def send(self,data):
        self.fire_down_stream(data[::-1])
        
class Exibir(Listener):

    def __init__(self, prefix = '>'):
        self.prefix = prefix

    def next(self,data):
        print('{}: {}'.format(self.prefix,str(data)))

Camada1 = CamadaNormal
Camada2 = CamadaInvertida
c1 = Camada1()
c2 = Camada2()
c1.inferior.add_listener(Exibir('Normal'))
c1.superior.add_listener(Exibir('c1^'))
c2.inferior.add_listener(Exibir('Invertido'))
c2.superior.add_listener(Exibir('c2^'))
Camada.connect_all(c1,c2)
c1.send("mensagem1")