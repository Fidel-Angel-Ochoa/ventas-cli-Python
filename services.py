import csv  # modulo para manejar archivos csv
import os
from clients.models import Client # con esto importamos la clase Client(con el formato que tendran nuestros clientes y la cabecera de tabla) que usaremos para crear nuestros clientes. esto se importa del archivo "models.py" de la carpeta "clients"


class ClientService:

    def __init__(self, table_name):  # creamos el nombre de nuestra tabla de clientes, nuestro archivo csv. Cuando llamemos a la clase "ClientService" de daremos como parametro el archivo csv y se ejecutaran las funciones que contiene esta clase
        self.table_name = table_name
    
    def create_client(self, client):  #el parametro "client" al parecer sera dado con posterioridad
        with open(self.table_name, mode = 'a') as f: # mode = "a" significa modo append, añadiremos nuevas filas conforme lo nesecitemos
            writer = csv.DictWriter(f, fieldnames = Client.schema()) # escribiremos en nuestro archivo "f", definimos las comlumnas de nuestra tabla con "fieldnames" que tomamos de la clase "Client" del metodo estatico "schema" creada en el archivo "models" y que importamos al inicio de este archivo
            writer.writerow(client.to_dict())  # escribimos en el archivo una fila, "DictWriter" necesita diccionarios por lo que el parametro "client" lo pasamos a "to_dict"(funcion que creamos en el archivo models para convetir strings a diccionarios) y lo convertimos en diccionario.

    
    # vamos a leer que clientes tenemos actualmente en nuesta base de datos con la siguiente funcion
    def list_clients(self):
        with open(self.table_name, mode = 'r') as f: # abrimos nuestro archivo, table_name hace referencia al nombre de nuestro archivo, es cual esta en la misma carpeta que este archivo y el resto.
            reader = csv.DictReader(f, fieldnames = Client.schema()) # leemos los datos que tenemos en nuestro archivo, tambien los nombres de la cebeceras que usaremos en la tabla que mostraremos y los guardamos en la variable "reader"

            return list(reader) # trasnformamos la variable "reader" a una lista para poder usarlo posteriormente en la interfaz para mostrar nuestros clientes.

    def update_client(self, updated_client):
        clients = self.list_clients()

        updated_clients = []
        for client in clients:
            if client['uid'] == updated_client.uid:
                updated_clients.append(updated_client.to_dict())
            else:updated_clients.append(client)

        self._save_to_disk(updated_clients)

    def _save_to_disk(self, clients):
        tmp_table_name = self.table_name +'.tmp'
        with open(tmp_table_name, mode = 'w') as f:  # no se requiere poner "self" antes de tmp_table_name por que se definio sin el en la linea anterior.
            writer = csv.DictWriter(f, fieldnames=Client.schema())
            writer.writerows(clients)

        os.remove(self.table_name)
        os.rename(tmp_table_name, self.table_name)