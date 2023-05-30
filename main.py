import sys
from typing import Collection
import csv
import os
from prettytable import  PrettyTable


CLIENT_TABLE = '.client.csv'
CLIENT_SCHEMA = ['name', 'company', 'email', 'position']
clients = []


def _initialize_clients_from_storage():
    with open(CLIENT_TABLE, mode = 'r') as f:
        reader = csv.DictReader(f, fieldnames = CLIENT_SCHEMA)

        for row in reader:
            clients.append(row)

    
def _save_client_to_storage(): # esta funcion guarda en el archivo .csv las modificaciones hechas en la lista de los clientes y cierra la base de datos.
    tmp_table_name = f'{CLIENT_TABLE}.tmp' #carga la tabla modificada en un archivo temporal
    with open(tmp_table_name, mode = 'w') as f: #abrimos el archivo
        writer = csv.DictWriter(f, fieldnames = CLIENT_SCHEMA) # creamos las columnas mediante el comando "DictWriter" para crear diccionarios, tomando los nombres de "CLIENTE_SCHEMA"
        writer.writerows(clients) # Creamos las filas con los datos que contiene la variable "clientes"

        os.remove(CLIENT_TABLE) # removemos el archivo que contiene CLIENT_TABLE que es la base de datos original
        os.rename(tmp_table_name, CLIENT_TABLE) # renombramos la tabla "tmp_table_name" que contiene la nueva informacion de los clientes con el nombre que tenia la tabla original CLIENT_TABLE, asi terminamos de remplazar la tabla sin modidifcar por una con nueva informacion.

def create_client(client):
    global clients
    
    if client not in clients:
        clients.append(client)
    else:
        print(f'The {client.get("name")}is already in the client\'s list')


def list_clients():
    # FORMATO DE TABLA CON PRETTYTABLE:
    client_table_format = PrettyTable()
    client_table_format.field_names = ['uid',CLIENT_SCHEMA[0],CLIENT_SCHEMA[1],CLIENT_SCHEMA[2],CLIENT_SCHEMA[3]]
    for idx, client in enumerate(clients):
        row = ([idx,client.get('name'),client.get('company'), client.get('email'), client.get('position')])
        client_table_format.add_rows([row])
    
    print(client_table_format)

    # MANERA ALTERNA DE HACERLO 1:
    # for idx, client in enumerate(clients):
    #     print(f'{idx} | {client.get("name")} | {client.get("company")} | {client.get("email")} | {client.get("position")}')
        
    # MANERA ALTERNA DE HACERLO 2:
        # print('{uid} | {name} | {company} | {email} | {position}'
        # .format(uid=idx, 
        #     name=client['name'],
        #     company=client['company'],
        #     email=client['email'],
        #     position=client['position']))


def search_client(client_name):  # funcion para buscar y confirmar la existencia de un cliente.
    global clients

    index = [0]
    found = False
    for idx,client in enumerate(clients):  # enumerate devuelve los valores "indice idx" y "clients" que hay en ese indice correspondiente y los guarda en "client".
        for name in client.values():  # idx es el indice de los diccionarios con los datos de los clientes en "clients" y al llamarlo aqui podemos llamar a los valores que contiene con el metodo ".values()", por que hace referencia automatica a esta lista anidada.
            if client_name == name:
                found = True
                index = int(idx)
                return found, index
            
    return found, index # regresa dos valores despues de generar todas las iteraciones y no encontrar nada


def update_client(client_name):
    global clients

    client_found, index = search_client(client_name)  # se hace swaping para retomar los dos valores que se genero en la funcion: un booleano y un indice numerico
    if client_found:
        update_client_fields = {
            'name': _get_client_field('name'),
            'company': _get_client_field('company'),
            'email': _get_client_field('email'),
            'position': _get_client_field('position'),
        }  
        clients[index] = update_client_fields
    else:
        _not_client_found(client_name)


def delete_client(client_name):
    global clients

    client_found, index = search_client(client_name)
    if client_found:
        clients.pop(index) # elimina todo el diccionario con los datos del cliente en el index señalado
    else:
        _not_client_found(client_name)


def _print_welcome():
    print('\nWELCOME TO PLATZI VENTAS')
    print('*' * 50)
    print('what would you like to do today? ')
    print('[C]reate client')
    print('[L]ist clients')
    print('[U]pdate client')
    print('[D]elete client')
    print('[S]earch client')

def _get_client_field(field_name):
    field = None
    while not field:
        field = input(f'What is the client {field_name}?')
    
    return field
    

def _get_client_name(action):
    client_name = None

    while not client_name:
        client_name = input((f'What is the client name to {action}?').strip() )

        if client_name == 'exit':
            client_name = None
            break
    if not client_name:
        sys.exit()

    return client_name


def _not_client_found(client_name):
    print(f'{client_name} is not in client list')


if __name__ == '__main__':
    _initialize_clients_from_storage()

    _print_welcome()
    
    command = input()
    command = command.upper()

    if command == 'C':
        client = {
            'name': _get_client_field('name'),
            'company': _get_client_field('company'),
            'email': _get_client_field('email'),
            'position': _get_client_field('position'),
        }
        create_client(client)
    elif command == 'L': #LISTO*******
        list_clients()
    elif command == 'U': #LISTO*******
        action = 'Update'
        client_name = _get_client_name(action)
        update_client(client_name)
    elif command == 'D': #LISTO*******
        action = 'Delete'
        client_name = _get_client_name(action)
        delete_client(client_name)        
    elif command == 'S': #LISTO*******
        action = 'Search'
        client_name = _get_client_name(action)
        client_found, index = search_client(client_name)  # esta variable toma ambos valores que la funcion devuelve

        if client_found: # tres opciones de imprimir los resultados
            print(f'The {client_name} is in the client\'s list')
            # print(f'{index}: {clients[index].get("name")}:{clients[index].get("company")}:{clients[index].get("email")}:{clients[index].get("position")}')
            # print(f'{index}: {clients[index].values()}')
            print(f'{index}: {clients[index]}')
        else:
            _not_client_found(client_name)
    else:
        print('Invalid command')

    _save_client_to_storage() # esta funcion guarda en el archivo .csv las modificaciones hechas en la lista de los clientes y cierra la base de datos.