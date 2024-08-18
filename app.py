from flask import Flask, jsonify, request
import os
import mysql.connector

app = Flask(__name__)

# Configurar la conexión a la base de datos MySQL
db_config = {
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Ruta de ejemplo para verificar disponibilidad
@app.route('/disponibilidad', methods=['GET'])
def disponibilidad():
    dia = request.args.get('dia')
    id_sala = request.args.get('id_sala')
    
    # Ejemplo de consulta a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT hora_inicio, hora_fin FROM reservas WHERE fecha = %s AND id_sala = %s", (dia, id_sala))
    resultados = cursor.fetchall()
    connection.close()
    
    horarios_disponibles = {
        "dia": dia,
        "id_sala": id_sala,
        "horarios": [f"{r[0]}-{r[1]}" for r in resultados]
    }

    return jsonify(horarios_disponibles)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
