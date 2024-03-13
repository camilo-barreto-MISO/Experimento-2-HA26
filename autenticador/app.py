from flask import Flask, request, jsonify ,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import IntegrityError
from enum import Enum
from flask_jwt_extended import create_access_token,JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
db = SQLAlchemy()
db.init_app(app)
jwt = JWTManager(app)


class TipoUsuario(Enum):
    BASICO = 'basico'
    PREMIUM = 'premium'

class Usuario(db.Model):
    __table_args__ = (UniqueConstraint('usuario', name='unique_username'),)
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    contrasenia = db.Column(db.String(50), nullable=False)
    tipo_usuario = db.Column(db.Enum(TipoUsuario), nullable=False, default=TipoUsuario.BASICO)

def crear_token(usuario):
        additional_claims = {"tipo_usuario":usuario.tipo_usuario.value} 
        return create_access_token(identity=usuario.id,additional_claims=additional_claims)

def crear_usuario_nuevo(usuario):
     try:
          db.session.add(usuario)
          db.session.commit()
          token = crear_token(usuario)
          return {"mensaje": "usuario creado", "token": token, "id": usuario.id}, 201
     except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Ya existe un usuario con este identificador"}, 400
     

@app.route('/crear_usuario', methods=['POST'])
def  crear_usuario():
    datos = request.get_json()

    if 'usuario' not in datos or 'contraseña' not in datos:
        return jsonify({'error':'Usuario y contraseña son obligatorios'}) , 400
    
    tipo_usuario = datos.get('tipo_usuario',TipoUsuario.BASICO.value)
    if tipo_usuario not in [item.value for item in TipoUsuario]:
        return jsonify({'error': 'Tipo de usuario no válido'}), 400
    
    usuario_nuevo = Usuario(usuario = datos['usuario'],contrasenia=datos['contraseña'],tipo_usuario=TipoUsuario(tipo_usuario))
    return crear_usuario_nuevo(usuario_nuevo)
    
@app.route('/autenticar',methods=['GET'])
def autenticar():
     if 'usuario' not in request.headers or 'contrasenia' not in request.headers:
          return make_response('Encabezados usuario y/o contraseña faltantes', 401)
     
     usuario = Usuario.query.filter(Usuario.usuario == request.headers['usuario'] ,
                                    Usuario.contrasenia == request.headers['contrasenia'] ).first()
     if usuario is None:
            return make_response('Verifique los datos ingresados', 401)
     token = crear_token(usuario=usuario)
     respuesta =  make_response({"mensaje": "usuario autenticado"},200)
     respuesta.headers['Authorization'] = f"Bearer {token}"
     return  respuesta
     


with app.app_context():
    db.create_all()


