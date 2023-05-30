import uuid  #modulo para crear "id" unicas automaticamente

class Client:
    def __init__(self, name, company, email, position, uid = None):
        self.name = name
        self.company = company
        self.email = email
        self.position = position
        self.uid = uid or uuid.uuid4()  # tomamos el uid que se nos proporcione, si no se nos proporciona generamos uno mediante el modulo uuid, uuid4 es un estandar en la industria para generar id unicos. los id son nesesarios en una base de datos como indentificadores

    def to_dict(self):
        return vars(self)  # la funcion global "vars" nos permite acceder a una representacion en diccionario de nuestro objeto que hemos construido(la clase Client) ya que para poder guardarlo en formato "csv" es necesario que sea un diccionario.

    @staticmethod # este decorador permite tener una funcion sin que sea parte "implicita" de la clase y no necesita recibir un primer argumento implicito como "self"
    def schema(): # esta funcion nos ayuda a establecer lo que ira en la cabecera de nuestra tabla con los datos de los clientes, solo nos ayudara a crear la cabecera de la tabla de clientes.
        return ['name', 'company', 'email', 'position', 'uid']
