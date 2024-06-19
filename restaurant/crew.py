# imports do Python
from threading import Thread, Semaphore

from restaurant.shared import (
    get_totem,
    get_client_by_ticket,
    get_chef,
    get_client_cont
)

"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""
class Crew(Thread):

    # Semaforo compartilhado entre as threads crew
    clients_waiting = Semaphore(0)
    # Libera todos as threads
    def release(n):
        for _ in range(n):
            Crew.clients_waiting.release()

    """ Inicia o membro da equipe com um id (use se necessario)."""
    def __init__(self, id):
        super().__init__()
        self._id = id
        # Insira o que achar necessario no construtor da classe.
        self.serving_client = None # Thread Cliente sendo atendido

    """ O membro da equipe espera um cliente. """    
    def wait(self):
        print("O membro da equipe ({}) está esperando um cliente.".format(self._id))
        # Espera um cliente chegar
        self.clients_waiting.acquire()
    
    # Pega o menor ticket na fila
    def get_ticket(self):
        totem = get_totem()
        with totem.access:
            ticket = totem.call.pop(0)
        return ticket
    
    """ O membro da equipe chama o cliente da senha ticket."""
    def call_client(self, ticket):
        # Busca o cliente pelo ticket
        self.serving_client = get_client_by_ticket(ticket)
        print(f"[CALLING] - O membro da equipe ({self._id}) \
está chamando o cliente da senha ({ticket}).")
        # Sinaliza para o cliente que ele pode fazer o pedido
        self.serving_client.can_procede.release()

    def make_order(self, order):
        # Espera o cliente pensar e fazer o pedido
        self.serving_client.made_order.acquire()
        print(f"[STORING] - O membro da equipe ({self._id}) está anotando\
o pedido ({order}) para o chef.")
        # Adiciona o pedido na fila do chef
        chef = get_chef()
        with chef.access_queue:
            chef.orders_queue.append(order)
        # Sinaliza para o chef que ha mais um pedido
        chef.orders.release()


    # Pega o ticket na fila

    """ Thread do membro da equipe."""
    def run(self):
        while True:
            self.wait()
            # Se nao houver mais clientes finaliza
            if get_client_cont() <= 0: break
            ticket = self.get_ticket()
            self.call_client(ticket)
            self.make_order(ticket)