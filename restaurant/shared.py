# Espaco reservado para voce inserir suas variaveis globais.
# Voce pode inserir como funcao (exemplo): 
# 
#  my_global_variable = 'Awesome value'
#  def get_my_global_variable():
#       global my_global_variable
#       return my_global_variable

# CONSTANTS
# General
N_THREADS = None

# Clients
MAX_THINKING_TIME = 3 # s
MIN_THINKING_TIME = 1 # s

MAX_EATING_TIME = 4
MIN_EATING_TIME = 1

# Chef
MAX_PREP_TIME = 5 # s
MIN_PREP_TIME = 1 # s


# Totem
totem = None
def get_totem():
    global totem
    return totem

# Table
table = None
def get_table():
    global table
    return table

# Chef
chef = None
def get_chef():
    global chef
    return chef

# Crew class
crew = None

# Clients
# Lista de clientes global
clients = None
# Retorna o cliente pelo ticket
def get_client_by_ticket(tiket):
    global clients
    for c in clients:
        if c.ticket == tiket:
            return c
    return None
# Numero de clientes a ser atendido
client_cont = 1000
client_cont_mutex = None
# Client cont decrementer
def decrement_client_cont():
    global client_cont
    with client_cont_mutex:
        client_cont -= 1

def get_client_cont():
    global client_cont
    with client_cont_mutex:
        return client_cont

# Finaliza toodas as threads em loop
def release_all():
    chef.orders.release()
    crew.release_all(N_THREADS) # N_THREADS com certeza maior que threads crew
        
