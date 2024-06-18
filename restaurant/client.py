# imports do Python
from threading import Thread, Semaphore
from time import sleep
from random import random

# imports do projeto
from restaurant.shared import get_totem, get_table

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
        print("[TICKET] - O cliente {} pegou o ticket.".format(self._id))

    """ Espera ser atendido pela equipe. """
    def wait_crew(self):
        print("[WAIT] - O cliente {} esta aguardando atendimento.".format(self._id))
        self.can_procede.acquire()

    
    """ O cliente pensa no pedido."""
    def think_order(self):
        print("[THINK] - O cliente {} esta pensando no que pedir.".format(self._id))
        sleep(random())

    """ O cliente faz o pedido."""
    def order(self):
        print("[ORDER] - O cliente {} pediu algo.".format(self._id))
        self.made_order.release()

    """ Espera pelo pedido ficar pronto. """
    def wait_chef(self):
        print("[WAIT MEAL] - O cliente {} esta aguardando o prato.".format(self._id))
        self.can_procede.acquire()
    
    """
        O cliente reserva o lugar e se senta.
        Lembre-se que antes de comer o cliente deve ser atendido pela equipe, 
        ter seu pedido pronto e possuir um lugar pronto pra sentar. 
    """
    def seat_and_eat(self):
        table = get_table()
        print("[WAIT SEAT] - O cliente {} esta aguardando um lugar ficar livre".format(self._id))
        table.seat()
        print("[SEAT] - O cliente {} encontrou um lugar livre e sentou".format(self._id))
        # Simula o cliente comendo
        sleep(random())
        #

    """ O cliente deixa o restaurante."""
    def leave(self):
        table = get_table()
        table.leave(self)
        print("[LEAVE] - O cliente {} saiu do restaurante".format(self._id))
    
    """ Thread do cliente """
    def run(self):
        self.get_my_ticket()
        self.wait_crew()
        self.think_order()
        self.order()
        self.wait_chef()
        self.seat_and_eat()
        self.leave()