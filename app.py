from flask import Flask, jsonify, request
from flask_cors import CORS      
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)

# BBDD
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/producto'

# user:clave@URLBBDD/nombreBBDD

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False # none
db= SQLAlchemy(app)                                # crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)                                # crea el objeto ma de de la clase Marshmallow


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Float())
    stock = db.Column(db.Integer())
    imagen = db.Column(db.String(400))

    def __init__ (self,nombre,precio,stock,imagen):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.imagen = imagen

# Resto de las tablas

with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ********************
class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock','imagen')

producto_schema=ProductoSchema()            # El objeto producto_schema es para traer un producto
productos_schema=ProductoSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto



@app.route('/productos', methods=['GET'])
def get_productos():
    all_productos = Producto.query.all()    # todos los productos de la base de datos
    result = producto_schema.dump(all_productos)
    return jsonify(result)


@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)   # retorna el JSON de un producto recibido como parametro


@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)


@app.route('/productos',methods=['POST']) # CREA UN REGISTRO
def create_producto():
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']
    nuevo_producto = Producto(nombre, precio, stock, imagen)
    db.session.add(nuevo_producto)
    db.session.commit()
    return producto_schema.jsonify(nuevo_producto)


@app.route('/productos/<id>',methods=['PUT']) # MODIFICAR
def update_producto(id):
    producto = Producto.query.get(id)
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']

    producto.nombre = nombre
    producto.precio = precio
    producto.stock = stock
    producto.imagen = imagen

    db.session.commit()
    return producto_schema.jsonify(producto)

if __name__ == '__main__':
    app.run(debug=True, port=5000)