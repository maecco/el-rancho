# imports do Python
from threading import Thread, Semaphore, Lock
from time import sleep
from random import randint

from restaurant.shared import get_client_by_ticket, get_client_cont

# Chef Constants
MAX_PREP_TIME = 5 # s
MIN_PREP_TIME = 1 # s

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
        with self.access_queue:
            self.current_order = self.orders_queue.pop(0)
        print("[COOKING] - O chefe esta preparando o pedido para a senha ({}).".format(self.current_order)) # Modifique para o numero do ticket
        sleep(randint(MIN_PREP_TIME,MAX_PREP_TIME))

    """ Chef serve o pedido preparado."""
    def serve(self):
        print("[READY] - O chefe está servindo o pedido para a senha ({}).".format(self.current_order)) # Modificar para o numero do ticket
        client = get_client_by_ticket(self.current_order)
        client.can_procede.release()

    """ O chefe espera algum pedido vindo da equipe."""
    def wait_order(self):
        print("O chefe está esperando algum pedido.")
        self.orders.acquire()
        

    """ Thread do chefe."""
    def run(self):
        while True:
            self.wait_order()
            # Se nao houver mais clientes termina as atividades
            if get_client_cont() <= 0: break
            self.cook()
            self.serve()