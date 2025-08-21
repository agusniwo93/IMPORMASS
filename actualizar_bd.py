import sqlite3

# Conectar a la base de datos existente
conexion = sqlite3.connect("facturador.db")
cursor = conexion.cursor()

# Intentamos agregar la nueva columna 'cantidad' si no existe
try:
    cursor.execute("ALTER TABLE productos ADD COLUMN cantidad INTEGER DEFAULT 0")
    print("✅ Columna 'cantidad' agregada correctamente.")
except sqlite3.OperationalError as e:
    print("⚠️ Ya existe la columna o hubo un error:", e)

# Guardar cambios y cerrar conexión
conexion.commit()
conexion.close()
