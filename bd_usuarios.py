import sqlite3

def crear_tabla_usuarios():
    conexion = sqlite3.connect("facturador.db")
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            clave TEXT NOT NULL
        )
    ''')

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tabla_usuarios()
    print("Tabla 'usuarios' creada correctamente.")
