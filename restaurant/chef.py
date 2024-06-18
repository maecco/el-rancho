# imports do Python
from threading import Thread, Semaphore, Lock
from time import sleep
from random import randint

from restaurant.shared import get_client_by_ticket

"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""
class Chef(Thread):
    
    def __init__(self):
        super().__init__()
        # Insira o que achar necessario no construtor da classe.
        self.orders_queue = list()
        self.access_queue = Lock()
        self.orders = Semaphore(0)
        self.current_order = None

    """ Chef prepara um dos pedido que recebeu do membro da equipe."""
    def cook(self):
        print("[COOKING] - O chefe esta preparando o pedido para a senha {}.".format(self.current_order)) # Modifique para o numero do ticket
        sleep(randint(1,5))

    """ Chef serve o pedido preparado."""
    def serve(self):
        print("[READY] - O chefe está servindo o pedido para a senha {}.".format(self.current_order)) # Modificar para o numero do ticket
        client = get_client_by_ticket(self.current_order)
        client.can_procede.release()

    """ O chefe espera algum pedido vindo da equipe."""
    def wait_order(self):
        print("O chefe está esperando algum pedido.")
        self.orders.acquire()
        self.current_order = self.orders_queue.pop(0)

    """ Thread do chefe."""
    def run(self):
        self.wait_order()
        self.cook()
        self.serve()