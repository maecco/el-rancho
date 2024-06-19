# imports do Python
from threading import Thread, Semaphore
from time import sleep
from random import randint

# imports do projeto
from restaurant.shared import (
    get_totem,
    get_table,
    decrement_client_cont,
    get_client_cont,
    release_all,
    )

# Client Constants
MAX_THINKING_TIME = 3 # s
MIN_THINKING_TIME = 1 # s
MAX_EATING_TIME = 4
MIN_EATING_TIME = 1

"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""
class Client(Thread):
    
    """ Inicializa o cliente."""
    def __init__(self, i):
        self._id = i
        super().__init__()
        # Insira o que achar necessario no construtor da classe.
        self.ticket = None
        self.can_procede = Semaphore(0)
        self.made_order = Semaphore(0)

    """ Pega o ticket do totem."""
    def get_my_ticket(self):
        # Encontra o totem
        totem = get_totem()
        # Espera o acesso ao totem e pega o ticket
        with totem.access:
            self.ticket = totem.get_ticket()
        print(f"[TICKET] - O cliente ({self._id}|{self.ticket}) pegou o ticket.")

    """ Espera ser atendido pela equipe. """
    def wait_crew(self):
        print(f"[WAIT] - O cliente ({self._id}|{self.ticket}) esta aguardando atendimento.")
        self.can_procede.acquire()

    
    """ O cliente pensa no pedido."""
    def think_order(self):
        print(f"[THINK] - O cliente ({self._id}|{self.ticket}) esta pensando no que pedir.")
        sleep(randint(MIN_THINKING_TIME,MAX_THINKING_TIME))

    """ O cliente faz o pedido."""
    def order(self):
        print(f"[ORDER] - O cliente ({self._id}|{self.ticket}) pediu algo.")
        self.made_order.release()

    """ Espera pelo pedido ficar pronto. """
    def wait_chef(self):
        print(f"[WAIT MEAL] - O cliente ({self._id}|{self.ticket}) esta aguardando o prato.")
        self.can_procede.acquire()
    
    """
        O cliente reserva o lugar e se senta.
        Lembre-se que antes de comer o cliente deve ser atendido pela equipe, 
        ter seu pedido pronto e possuir um lugar pronto pra sentar. 
    """
    def seat_and_eat(self):
        table = get_table()
        print(f"[WAIT SEAT] - O cliente \
({self._id}|{self.ticket}) esta aguardando um lugar ficar livre")
        table.seat(self)
        print(f"[SEAT] - O cliente \
({self._id}|{self.ticket}) encontrou um lugar livre e sentou")
        # Simula o cliente comendo
        sleep(randint(MIN_EATING_TIME, MAX_EATING_TIME))
        #

    """ O cliente deixa o restaurante."""
    def leave(self):
        table = get_table()
        table.leave(self)
        print(f"[LEAVE] - O cliente ({self._id}|{self.ticket}) saiu do restaurante")
        # Decrementa o numero de clientes
        decrement_client_cont()
        # Se é o ultimo cliente, libera todas as threads
        if get_client_cont() == 0:
            release_all()
    
    """ Thread do cliente """
    def run(self):
        self.get_my_ticket()
        self.wait_crew()
        self.think_order()
        self.order()
        self.wait_chef()
        self.seat_and_eat()
        self.leave()
