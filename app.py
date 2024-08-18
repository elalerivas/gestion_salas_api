from flask import Flask, jsonify, request
import os
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Configurar la conexión a la base de datos
db_config = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Ruta de ejemplo para verificar disponibilidad
@app.route('/disponibilidad', methods=['GET'])
def disponibilidad():
    dia = request.args.get('dia')
    id_sala = request.args.get('id_sala')
    
    # Aquí implementamos la lógica para consultar la base de datos de reservas
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT hora_inicio, hora_fin 
    FROM reservas 
    WHERE fecha = %s AND id_sala = %s
    """
    cursor.execute(query, (dia, id_sala))
    horarios_ocupados = cursor.fetchall()
    
    # Lógica para determinar los horarios disponibles
    horarios_disponibles = calcular_horarios_disponibles(horarios_ocupados)

    cursor.close()
    conn.close()

    return jsonify(horarios_disponibles)

# Función para calcular horarios disponibles (puedes personalizarla)
def calcular_horarios_disponibles(horarios_ocupados):
    # Aquí deberías implementar la lógica para calcular horarios disponibles
    # Basado en los horarios ocupados que se obtuvieron de la consulta.
    return {"horarios_disponibles": ["09:00-10:00", "14:00-15:00"]}

# Nueva ruta para reservar un turno
@app.route('/reservar', methods=['POST'])
def reservar():
    data = request.json
    id_sala = data.get('id_sala')
    fecha = data.get('fecha')
    hora_inicio = data.get('hora_inicio')
    hora_fin = data.get('hora_fin')
    numero_estudiantes = data.get('numero_estudiantes')
    tipo_actividad = data.get('tipo_actividad')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar si el turno ya está ocupado
    query = """
    SELECT * FROM reservas 
    WHERE fecha = %s AND id_sala = %s AND hora_inicio = %s
    """
    cursor.execute(query, (fecha, id_sala, hora_inicio))
    existing_reservation = cursor.fetchone()

    if existing_reservation:
        return jsonify({"error": "El turno ya está reservado"}), 409
    
    # Insertar la nueva reserva en la base de datos
    insert_query = """
    INSERT INTO reservas (id_sala, fecha, hora_inicio, hora_fin, numero_estudiantes, tipo_actividad)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (id_sala, fecha, hora_inicio, hora_fin, numero_estudiantes, tipo_actividad))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"success": "Turno reservado con éxito"}), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
