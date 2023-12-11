#ESTE ES EL QUE VAAAAAA!!!!!!!!!!!!!!!!!!!!
# Importa las clases Flask, jsonify y request del módulo flask
from flask import Flask, jsonify, request
# Importa la clase CORS del módulo flask_cors
from flask_cors import CORS
# Importa la clase SQLAlchemy del módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# Importa la clase Marshmallow del módulo flask_marshmallow
from flask_marshmallow import Marshmallow

# Crea una instancia de la clase Flask con el nombre de la aplicación
app = Flask(__name__)
# Configura CORS para permitir el acceso desde el frontend al backend
CORS(app)

# Configura la URI de la base de datos con el driver de MySQL, usuario, contraseña y nombre de la base de datos
# URI de la BD == Driver de la BD://user:password@UrlBD/nombreBD
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/proyecto"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/clientes" # Comentar en despliegue https://sofitarabusi.pythonanywhere.com/cliente
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://sofitarabusi:password@sofitarabusi.mysql.pythonanywhere-services.com/sofitarabusi$default" # Comentar en despliegue https://sofitarabusi.pythonanywhere.com/cliente
# Configura el seguimiento de modificaciones de SQLAlchemy a False para mejorar el rendimiento
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Crea una instancia de la clase SQLAlchemy y la asigna al objeto db para interactuar con la base de datos
db = SQLAlchemy(app)
# Crea una instancia de la clase Marshmallow y la asigna al objeto ma para trabajar con serialización y deserialización de datos
ma = Marshmallow(app)

class Cliente(db.Model):  # Cliente hereda de db.Model
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    apellido=db.Column(db.String(100))
    telefono=db.Column(db.Integer)
    localidad=db.Column(db.String(100))
    direccion=db.Column(db.String(400))
    bolson=db.Column(db.Integer)
    medio_de_pago=db.Column(db.String(45))
    dia_de_entrega=db.Column(db.String(45))

    def __init__(self, nombre, apellido, telefono, localidad, direccion, bolson, medio_de_pago, dia_de_entrega):
        self.nombre=nombre
        self.apellido=apellido
        self.telefono=telefono
        self.localidad=localidad 
        self.direccion=direccion
        self.bolson=bolson
        self.medio_de_pago=medio_de_pago
        self.dia_de_entrega= dia_de_entrega

# Se pueden agregar más clases para definir otras tablas en la base de datos

with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos

# Definición del esquema para la clase Cliente
class ClienteSchema(ma.Schema):

    class Meta:
        fields = ("id", "nombre", "apellido", "telefono", "localidad", "direccion", "bolson", "medio_de_pago", "dia_de_entrega")

cliente_schema = ClienteSchema()  # Objeto para serializar/deserializar un cliente
clientes_schema = ClienteSchema(many=True)  # Objeto para serializar/deserializar múltiples clientes

@app.route('/')
def index():
    return "<h1>API Ok!</h1>"

@app.route("/clientes", methods=["GET"])
def get_clientes():
    """
    Endpoint para obtener todos los productos de la base de datos.

    Retorna un JSON con todos los registros de la tabla de productos.
    """
    try:
        all_clientes = Cliente.query.all()  # Obtiene todos los registros de la tabla de cliente
        result = clientes_schema.dump(all_clientes)  # Serializa los registros en formato JSON
        return jsonify(result)  # Retorna el JSON de todos los registros de la tabla
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/clientes/<id>", methods=["GET"])
def get_cliente(id):
    """
    Endpoint para obtener un cliente específico de la base de datos.

    Retorna un JSON con la información del producto correspondiente al ID proporcionado.
    """
    try:
        cliente = Cliente.query.get(id)  # Obtiene el producto correspondiente al ID recibido
        if cliente:
            return cliente_schema.jsonify(cliente)  # Retorna el JSON del producto
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/clientes/<id>", methods=["DELETE"])
def delete_cliente(id):
    """
    Endpoint para eliminar un cliente de la base de datos.

    Elimina el producto correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    try:
        cliente = Cliente.query.get(id)  # Obtiene el cliente correspondiente al ID recibido
        if cliente:
            db.session.delete(cliente)  # Elimina el cliente de la sesión de la base de datos
            db.session.commit()  # Guarda los cambios en la base de datos
            return cliente_schema.jsonify(cliente)  # Retorna el JSON del cliente eliminado
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/clientes", methods=["POST"])  # Endpoint para crear un cliente
def create_cliente():
    try:
        # Validación de entrada
        required_fields = ["nombre", "apellido", "telefono", "localidad", "direccion", "bolson", "medio_de_pago", "dia_de_entrega"]
        for field in required_fields:
            if field not in request.json:
                return jsonify({"error": f"Campo '{field}' es requerido"}), 400

        nombre = request.json["nombre"]
        apellido = request.json["apellido"]
        telefono = int(request.json["telefono"])
        localidad = request.json["localidad"]
        direccion = request.json["direccion"]
        bolson = int(request.json["bolson"])
        medio_de_pago = request.json["medio_de_pago"]
        dia_de_entrega = request.json["dia_de_entrega"]

        new_cliente = Cliente(nombre, apellido, telefono, localidad, direccion, bolson, medio_de_pago, dia_de_entrega)  # Crea un nuevo objeto Cliente con los datos proporcionados
        db.session.add(new_cliente)  # Agrega el nuevo cliente a la sesión de la base de datos
        db.session.commit()  # Guarda los cambios en la base de datos
        return cliente_schema.jsonify(new_cliente)  # Retorna el JSON del nuevo cliente creado
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/clientes/<id>", methods=["PUT"])  # Endpoint para actualizar un cliente
def update_cliente(id):
    try:
        cliente = Cliente.query.get(id)  # Obtiene el cliente existente con el ID especificado

        if cliente:
            # Actualiza los atributos del cliente con los datos proporcionados en el JSON
            cliente.nombre = request.json["nombre"]
            cliente.apellido = request.json["apellido"]
            cliente.telefono = request.json["telefono"]
            cliente.localidad = request.json["localidad"]
            cliente.direccion = request.json["direccion"]
            cliente.bolson = request.json["bolson"]
            cliente.medio_de_pago = request.json["medio_de_pago"]
            cliente.dia_de_entrega = request.json["dia_de_entrega"]

            db.session.commit()  # Guarda los cambios en la base de datos
            return cliente_schema.jsonify(cliente)  # Retorna el JSON del cliente actualizado
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
# Programa Principal: Solo para uso local - Comentar en despliegue -
# Ejecuta el servidor Flask en el puerto 5000 en modo de depuración
if __name__ == "__main__":
    app.run(debug=True, port=5000)