from .connection import get_conn

DDL = """
CREATE TABLE IF NOT EXISTS usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  usuario TEXT NOT NULL UNIQUE,
  clave   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  codigo TEXT UNIQUE,
  precio REAL NOT NULL,
  cantidad INTEGER NOT NULL DEFAULT 0,
  descripcion TEXT
);
"""

def init_schema():
    with get_conn() as conn:
        conn.executescript(DDL)

if __name__ == "__main__":
    init_schema()
    print("Esquema OK")
