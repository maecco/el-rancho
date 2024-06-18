# Espaco reservado para voce inserir suas variaveis globais.
# Voce pode inserir como funcao (exemplo): 
# 
#  my_global_variable = 'Awesome value'
#  def get_my_global_variable():
#       global my_global_variable
#       return my_global_variable

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
