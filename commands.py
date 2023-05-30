import click
#from click.termui import prompt

from clients.services import ClientService
from clients.models import Client

"""modificamos los comandos que usaremos dentro del grupo clientes.
   Estamos creando una interfaz de usuario, recreando el programa
   de "Platzi ventas" que programamos anteriormente pero ahora en
   una interfas de linea de comandos, basada en texto.

    IMPORTANTE
    Para llamar y utilizar esta interfaz de linea de comando
    escribiremos en la terminal "pv clients + nombre_del_comando"
    para que funcione deveremos estar en la carpeta que contiene
    el archivo "pv.py" y "setup.py", si escribes "pve clients" podras
    ver los comandos que se pueden utilizar.
"""


# para convertir las funciones siguientes en comandos de click usamos los decoradores
@click.group() # este decorador hace a la funcion "clients" otro decorador, para luego usarlos como comandos
def clients():
    """Manage the clients lifecycle"""
    pass


@clients.command()  #con este decorador estamos diciendo que la funcion("create") es un comando de nuestra funcion "clients" (grupo de comandos)
@click.option('-n', '--name', 
            type=str,
            prompt=True,
            help = 'The client name') # "option" es un decorador de "click" la cua nos ayuda a establecer opciones para nuestro comando, primero recibe todos los valores posionales que queramos declarar(texto, numeros, otras variables), luego recibe "keywords", es decir, palabras clave como funciones del sistema o metodos, ejemplo "type" define que tipo de parametros espera recibir. En este caso los dos primeros argumentos establecen exactamente que texto espera recibir, luego "type" establece que sera texto, "prompt" es similar al metodo "input" y permite que el usuario ingrese algun argumento, lo que habilita que el usuario ingrese alguna de las respuestas esperadas. por ultimo "help" donde se declara una sentencia a mostrar. esta funcionalidad se agrega a "def create(...)"
@click.option('-c', '--company', 
            type=str,
            prompt=True,
            help = 'The client company')
@click.option('-e', '--email', 
            type=str,
            prompt=True,
            help = 'The client email')
@click.option('-p', '--position', 
            type=str,
            prompt=True,
            help = 'The client position')
# en los decoradores "click.option" se iran ingresando los valores para name, company, email, position y en ese orden se pasaran a la funcion "def create(...)" por lo que tendremos nuestro argumentos que seran usados dentro del codigo de esta funcion.
@click.pass_context  #le pasamos el contexto que generamos anteriormente en otros archivos como en "pv.py", haremos lo mismo para las otras funciones.
def create(ctx, name, company, email, position):  # creamos que datos tendran nuestros clientes
    """Creates a new client"""
    client = Client(name, company, email, position) # llamamos la clase client declarada en "models.py" con sus parametros, a excepcion de "uid" el cliente en este punto no tiene id(cliente nuevo)
    client_service = ClientService(ctx.obj['clients_table'])  # pasamos el nombre de la tabla "clients_table" declarada en "pv.py" (contiene el nombre de nuestro archivo .csv) y se lo pasamos a la clase "ClientService"

    client_service.create_client(client) # con el archivo que obtenemos en "client_service" ahora tomaremos los datos que se ingresaron en "client"(name, company, email, position) y los pasaremos a la funcion "create_client" declarada en "services.py" donde se le dara formato y se guardara en el archivo .clients.csv creado en "pv.py"


@clients.command()
@click.pass_context
def list(ctx):
    """List all clients"""
    client_service = ClientService(ctx.obj['clients_table'])

    clients_list = client_service.list_clients()

    click.echo('ID |  NAME  |  COMPANY  |  EMAIL  |  POSITION') # click.echo muy similar a "print" pero con la diferencia que click.echo no varia su funcionamiento a travez de los distintos sistemas operativos.
    click.echo('*' * 100)

    for client in clients_list: # con este ciclo imprimimos en pantalla cada cliente que encontremos
        click.echo(f'{client["uid"]} | {client["name"]} | {client["company"]} | {client["email"]} | {client["position"]}')


@click.argument('client_uid', type=str) # decorador que nos ayuda ingresar un argumento, que la funcion reciba la uid del cliente, se ingresa en consola de la siguiente manera: "pv clients update id_que_quermos_cambiar"
@clients.command()
@click.pass_context
def update(ctx, client_uid):
    """Update a client"""
    client_service = ClientService(ctx.obj['clients_table'])  # obtenemos el nombre del archivo de la tabla

    client_list = client_service.list_clients()  # con el nombre del archivo abrimos la funcion list_clients y obtenemos la lista de clientes
    
    client = [client for client in client_list if client['uid'] == client_uid]

    if client:
        client = _update_client_flow(Client(**client[0]))
        client_service.update_client(client)

        click.echo('Client update')
    else:
        click.echo('client not found')


def _update_client_flow(client):
    click.echo('Leave empty if you dont want to modify the value')

    client.name = click.prompt('New name', type=str, default=client.name)
    client.company = click.prompt('New company', type=str, default=client.company)
    client.email = click.prompt('New email', type=str, default=client.email)
    client.position = click.prompt('New position', type=str, default=client.position)

    return client


@clients.command()
@click.pass_context
def delete(ctx, client_uid):
    """Delete a client"""
    pass


all = clients  # esto crea un alias de todos los comandos creados aqui.
