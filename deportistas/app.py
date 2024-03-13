from flask import Flask, jsonify, abort, request
from faker import Faker
from flask_jwt_extended import  jwt_required,JWTManager,verify_jwt_in_request,get_jwt
import random
import datetime

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
fake = Faker()
jwt = JWTManager(app)

def generar_enveto():
    fecha_actual = datetime.date.today()
    fecha_siguiente_mes = fecha_actual + datetime.timedelta(days=30)
    fecha_evento = fake.date_time_between_dates(datetime_start=fecha_actual,datetime_end=fecha_siguiente_mes)
    return{
        'fecha': fecha_evento.strftime('%d %B %Y %H:%M'),
        'lugar': fake.city(),
        'nombre': fake.catch_phrase()
    }
def verificar_permisos_usuario_premium():
    verify_jwt_in_request()
    jwt = get_jwt()
    if not jwt.get("tipo_usuario") == 'premium':
            abort(403, description="Debe ser un usuario premium para ejecutar esta acción.")


@app.route('/eventos', methods=['GET'])
@jwt_required()
def obtener_eventos():
    cantidad_eventos=random.randint(2, 10)
    eventos = []
    for _ in range(cantidad_eventos):
        eventos.append(generar_enveto())

    return jsonify(eventos),200

@app.route('/agendar',methods=['POST'])
@jwt_required()
def agendar():
    verificar_permisos_usuario_premium()
    datos = request.json
    return jsonify({'mensaje': f'Cita agendada exitosamente con el entrenador:{datos['entrenador']} para la fecha: {datos['fecha']} '}), 201