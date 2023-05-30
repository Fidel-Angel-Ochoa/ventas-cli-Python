import click

from clients import commands as clients_commands  # importamos los comandos de la funcion "clients" del archivo "commands.py", como si se llamaran "clients_commands"

CLIENTS_TABLE = '.clients.csv' # el nombre del archivo que se usara en "commands" y posterior mente en "services" para crear el archivo .csv que contendra nuestros clientes.


@click.group() # con este decorador le decimos a click que es nuetro punto de entrada
@click.pass_context # nos da un objeto contexto, lo agregaremos a la funcion como "ctx"
def cli(ctx):
    ctx.obj = {} # este objeto contexto lo inicializamos como un diccionario vacio
    ctx.obj['clients_table'] = CLIENTS_TABLE # Con esta linea se enlaza 'clients_table' que se usa en la funcion "create" en el archivo "commands", con CLIENTS_TABLE mediante el uso del "contexto"

cli.add_command(clients_commands.all) # añadimos a la funcion "cli" los comandos establecidos en el archivo "commands.py"