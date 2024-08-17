from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Ruta de ejemplo para verificar disponibilidad
@app.route('/disponibilidad', methods=['GET'])
def disponibilidad():
    dia = request.args.get('dia')
    id_sala = request.args.get('id_sala')
    
    # Aquí puedes implementar la lógica para consultar la base de datos de reservas
    horarios_disponibles = {
        "dia": dia,
        "id_sala": id_sala,
        "horarios": ["09:00-10:00", "14:00-15:00"]
    }

    return jsonify(horarios_disponibles)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
