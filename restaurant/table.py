from threading import Semaphore
"""
    Não troque o nome das variáveis compartilhadas, a assinatura e o nomes das funções.
"""
class Table:

    """ Inicia a mesa com um número de lugares """
    def __init__(self,number):
        self._number = number
        # Insira o que achar necessario no construtor da classe.
        self.seats = Semaphore(number) # Semaforo para controlar os lugares vagos

    """ O cliente se senta na mesa."""
    def seat(self, client):
        # Espera um lugar ficar livre
        self.seats.acquire()
    
    """ O cliente deixa a mesa."""
    def leave(self, client):
        # Libera um lugar
        self.seats.release()
