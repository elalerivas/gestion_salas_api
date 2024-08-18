import mysql.connector
from datetime import datetime, timedelta
import calendar

# Conectar a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PamelaSql531@",  # Reemplaza con tu contraseña de MySQL
    database="gestion_turnos"
)

# Crear un cursor
cursor = conexion.cursor()

# Eliminar la tabla turnos si ya existe
cursor.execute("DROP TABLE IF EXISTS turnos")

# Crear la tabla de turnos
cursor.execute("""
CREATE TABLE turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    semana INT NOT NULL,
    dia VARCHAR(50) NOT NULL,
    es_laborable BOOLEAN NOT NULL,
    fecha INT NOT NULL,
    mes VARCHAR(50) NOT NULL
)
""")

# Map from English to Spanish for days of the week
english_to_spanish_days = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes"
}
#
# Mapear desde el Ingles al Español los meses del año
english_to_spanish_months ={
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
}

# Rango de fechas: marzo a noviembre de 2024
start_date = datetime(2024, 3, 1)
end_date = datetime(2024, 11, 30)

current_date = start_date
week_number = 1

# Insertar turnos en la tabla
while current_date <= end_date:
    if current_date.weekday() < 5:  # De lunes (0) a viernes (4)
        dia_semana = calendar.day_name[current_date.weekday()]
        dia_semana_espanol = english_to_spanish_days[dia_semana]
        es_laborable = True  # Puedes ajustar esto según tu lógica de feriados
        mes_espanol = english_to_spanish_months[current_date.strftime("%B")]
        cursor.execute("""
        INSERT INTO turnos (semana, dia, es_laborable, fecha, mes)
        VALUES (%s, %s, %s, %s, %s)
        """, (week_number, dia_semana_espanol, es_laborable,current_date.day ,mes_espanol))

    if current_date.weekday() == 6:  # Si es domingo, incrementar el número de semana
        week_number += 1

    current_date += timedelta(days=1)

# Confirmar la transacción
conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()

print("Turnos generados exitosamente.")
