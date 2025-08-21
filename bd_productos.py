import sqlite3

def crear_base_de_datos():
    conexion = sqlite3.connect("facturador.db")
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigo TEXT,
            precio REAL NOT NULL,
            descripcion TEXT
        )
    ''')

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_base_de_datos()
    print("Base de datos y tabla 'productos' creadas correctamente.")
