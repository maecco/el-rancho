# imports do Python
from threading import Thread, Semaphore

from restaurant.shared import get_totem, get_client_by_ticket, get_chef

"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""
class Crew(Thread):

    # Semaforo compartilhado
    clients_waiting = Semaphore(0)

    """ Inicia o membro da equipe com um id (use se necessario)."""
    def __init__(self, id):
        super().__init__()
        self._id = id
        # Insira o que achar necessario no construtor da classe.
        self.serving_client = None

    """ O membro da equipe espera um cliente. """    
    def wait(self):
        print("O membro da equipe {} está esperando um cliente.".format(self._id))
        self.clients_waiting.acquire()
    
    # Pega o ticket na fila
    def get_ticket():
        totem = get_totem()
        with totem.queue_access:
            ticket = totem.call.pop(0)
        return ticket
    #
    """ O membro da equipe chama o cliente da senha ticket."""
    def call_client(self, ticket):
        self.serving_client = get_client_by_ticket(ticket)
        print("[CALLING] - O membro da equipe {} está chamando o cliente da senha {}.".format(self._id, ticket))
        self.serving_client.can_procede.release()

    def make_order(self, order):
        self.serving_client.made_order.acquire()
        print("[STORING] - O membro da equipe {} está anotando o pedido {} para o chef.".format(self._id, order))
        chef = get_chef()
        with chef.access_queue:
            chef.orders_queue.append(order)
        chef.orders.release()


    # Pega o ticket na fila

    """ Thread do membro da equipe."""
    def run(self):
        self.wait()
        ticket = self.get_ticket()
        self.call_client(ticket)
        self.make_order(ticket)