from typing import List

class Camada:
    cam_sup = None
    cam_inf = None

    @classmethod
    def connect_all(cls, *Camadas : List['Camada']):
        for a, b in zip(Camadas[:-1], Camadas[1:]):
            a.cam_inf.add_listener(b.cam_sup)
            b.cam_sup.add_listener(a.cam_inf)

    @classmethod
    def crossover(cls, a : 'Camada', b : 'Camada'):
        a.cam_inf.add_listener(b.cam_inf)
        b.cam_inf.add_listener(a.cam_inf)

class listener():
    def next(self, data):
        raise NotImplementedError()
        #erro = não implementado


class Interface(listener): 
    def next(self, data):
        raise NotImplementedError()

    def add_listener(self, listener : listener):
        raise NotImplementedError()

#letra por letra
class camadaBase(Camada):
    up = None
    down = None

    def __init__(self):
        self.up = []
        self.down = []

        Camada = self

        class intSuperior(Interface):
            
            def add_listener(self, listener : listener):
                Camada.up.append(listener)

            def next(self, data):
                Camada.send(data)


        self.cam_sup = intSuperior()

        class intInferior(Interface):
            
            def add_listener(self, listener : listener):
                Camada.down.append(listener)

            def next(self, data):
                Camada.receber(data)

        self.cam_inf = intInferior()

    def fire_up(self,data):
        for listener in self.up:
            listener.next(data)

    def fire_down(self,data):
        for listener in self.down:
            listener.next(data)

    def send(self,data):
        raise NotImplementedError()

    def receber(self,data):
        raise NotImplementedError()

class show(listener):
    def __init__(self, prefix = '>'):
        self.prefix = prefix

    def next(self,data):
        print('{}: {}'.format(self.prefix,str(data)))

class StringCamada(camadaBase):
    def receber(self,data):
        self.fire_up(data)

    def send(self,data):
        self.fire_down(data)

class ReverseCamada(camadaBase):
    def receber(self,data):
        self.fire_up(data[::-1])

    def send(self,data):
        self.fire_down(data[::-1])

class magic(camadaBase):
    buffer = None
    
    def __init__(self):
        super().__init__()
        self.buffer = []

    def receber(self,data):
        if data is None:
            self.fire_up(''.join(self.buffer))
            self.buffer = []
        else:
            self.buffer.append(data)

    def send(self,data):
        for c in data:
            self.fire_down(c)
        self.fire_down(None)

#definindo
Camada3 = StringCamada
Camada2 = ReverseCamada
Camada1 = magic
a3 = Camada3()
a2 = Camada2()
a1 = Camada1()
b3 = Camada3()
b2 = Camada2()
b1 = Camada1()

#exibir
a3.cam_inf.add_listener(show())
a3.cam_sup.add_listener(show())
a2.cam_inf.add_listener(show())
a2.cam_sup.add_listener(show())
a1.cam_inf.add_listener(show())
a1.cam_sup.add_listener(show())
b3.cam_inf.add_listener(show())
b3.cam_sup.add_listener(show())
b2.cam_inf.add_listener(show())
b2.cam_sup.add_listener(show())
b1.cam_inf.add_listener(show())
b1.cam_sup.add_listener(show())
Camada.connect_all(a3,a2,a1)
Camada.connect_all(b3,b2,b1)
Camada.crossover(a1,b1)

#send
a3.send("Pork")
b3.send("Tamago")