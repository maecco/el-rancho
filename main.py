# imports do Python
import sys
sys.dont_write_bytecode = True # Usado para nao criar arquivos .pyc
import argparse

# Imports necessarios para executar as threads
from restaurant.client import Client
from restaurant.crew import Crew
from restaurant.chef import Chef

from restaurant.totem import Totem
# Importe o que achar necessario aqui
# import my_module
from restaurant.table import Table
import restaurant.shared as shared

def definitions(argv, threads):
    """
    Esse espaco e reservado para voce definir variaveis globais que serao utilizadas por todas as threads.
    Lembre-se de criar as variaveis globais no arquivo restaurant/shared.py
    """
    # Totem
    shared.totem = Totem(argv.clients)
    # Table
    shared.table = Table(argv.seats)
    # Chef
    def get_chef():
        for t in threads:
            if isinstance(t, Chef):
                return t
    shared.chef = get_chef()
    # Clients
    def init_clients(threads):
        clients = list()
        for t in threads:
            if isinstance(t, Client):
                clients.append(t)
        return clients
    # Lista de clientes global
    shared.clients = init_clients(threads)

def close_all(argv, threads):
    """
    Esse espaco e reservado para voce fechar as coisas que voce abriu (se necessario).
    """
    pass


##################################################################################################
######                          Nao modifique o codigo abaixo                               ######
##################################################################################################
if __name__ == "__main__":

    args = argparse.ArgumentParser()
    
    # Argumentos para o programa (main.py --clients 10 --crew 5 --seats 5)

    args.add_argument("--clients", type=int, default=10, help="Numero de clientes que irao ao restaurante mexicano")
    args.add_argument("--crew", type=int, default=5, help="Numero de funcionarios do restaurante mexicano")
    args.add_argument("--seats", type=int, default=5, help="Quantidade de assentos na grande mesa do restaurante mexicano")

    # Parseando os argumentos
    argv = args.parse_args()

    # Verificando se os argumentos sao validos
    assert argv.clients > 0, "Numero de clientes deve ser maior que 0"
    assert argv.crew > 0, "Numero de funcionarios deve ser maior que 0"
    assert argv.seats > 0 and argv.seats < argv.clients, "Numero de assentos deve ser maior que 0 e menor que o numero de clientes"

   
    threads = list()

    threads.append(Chef())
    
    # Instanciando a equipe
    for id in range(argv.crew):
        threads.append(Crew(id))

    # Instanciando os clientes
    for id in range(argv.clients):
        threads.append(Client(id))

    # Iniciar as definições (variaveis globais)
    definitions(argv, threads)

    # Iniciando todas as threads
    for thread in threads:
        thread.start()

    # Finalizando todas as threads
    for thread in threads:
        thread.join()

    # Fechando modulos abertos
    close_all(argv, threads)

    print("[FIM] - Terminamos o dia! Abriremos amanha as 8:00.")
