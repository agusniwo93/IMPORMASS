from .connection import get_conn

DDL = """
CREATE TABLE IF NOT EXISTS usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  usuario TEXT NOT NULL UNIQUE,
  clave   TEXT NOT NULL,
  rol     TEXT NOT NULL DEFAULT 'vendedor'
);

CREATE TABLE IF NOT EXISTS productos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  codigo TEXT UNIQUE,
  precio REAL NOT NULL,
  cantidad INTEGER NOT NULL DEFAULT 0,
  descripcion TEXT
);

CREATE TABLE IF NOT EXISTS clientes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tipo_doc TEXT NOT NULL DEFAULT 'RUC',
  num_doc TEXT NOT NULL UNIQUE,
  razon_social TEXT NOT NULL,
  direccion TEXT,
  telefono TEXT,
  email TEXT
);

CREATE TABLE IF NOT EXISTS facturas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  serie TEXT NOT NULL DEFAULT 'F001',
  numero INTEGER NOT NULL,
  cliente_id INTEGER NOT NULL,
  moneda TEXT NOT NULL DEFAULT 'SOLES',
  fecha_emision TEXT NOT NULL,
  subtotal REAL NOT NULL DEFAULT 0,
  descuentos REAL NOT NULL DEFAULT 0,
  valor_venta REAL NOT NULL DEFAULT 0,
  igv REAL NOT NULL DEFAULT 0,
  isc REAL NOT NULL DEFAULT 0,
  icbper REAL NOT NULL DEFAULT 0,
  otros_cargos REAL NOT NULL DEFAULT 0,
  total REAL NOT NULL DEFAULT 0,
  estado TEXT NOT NULL DEFAULT 'EMITIDA',
  creado_en TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS factura_detalle (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  factura_id INTEGER NOT NULL,
  tipo TEXT NOT NULL DEFAULT 'Bien',
  afectacion TEXT NOT NULL DEFAULT 'Gravado',
  unidad TEXT NOT NULL DEFAULT 'UNIDAD',
  cantidad REAL NOT NULL,
  codigo TEXT,
  descripcion TEXT NOT NULL,
  valor_unit REAL NOT NULL,
  descuento REAL NOT NULL DEFAULT 0,
  subtotal REAL NOT NULL,
  igv REAL NOT NULL DEFAULT 0,
  isc REAL NOT NULL DEFAULT 0,
  icbper REAL NOT NULL DEFAULT 0,
  total REAL NOT NULL,
  FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS configuracion (
  clave TEXT PRIMARY KEY,
  valor TEXT NOT NULL DEFAULT ''
);
"""


def _migrate_roles(conn):
    """Agrega la columna 'rol' a usuarios si no existe (migración)."""
    cur = conn.execute("PRAGMA table_info(usuarios)")
    columnas = [row[1] for row in cur.fetchall()]
    if "rol" not in columnas:
        conn.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT NOT NULL DEFAULT 'vendedor'")


def _ensure_admin(conn):
    """Crea un usuario admin por defecto si no existe ningún admin."""
    import hashlib
    cur = conn.execute("SELECT 1 FROM usuarios WHERE rol='admin' LIMIT 1")
    if cur.fetchone() is None:
        hashed = hashlib.sha256("admin1234".encode()).hexdigest()
        try:
            conn.execute(
                "INSERT INTO usuarios (usuario, clave, rol) VALUES (?, ?, ?)",
                ("admin", hashed, "admin"),
            )
        except Exception:
            # Si el usuario 'admin' ya existe, actualiza su rol y clave
            conn.execute(
                "UPDATE usuarios SET rol='admin', clave=? WHERE usuario='admin'",
                (hashed,)
            )


def init_schema():
    with get_conn() as conn:
        conn.executescript(DDL)
        _migrate_roles(conn)
        _ensure_admin(conn)


if __name__ == "__main__":
    init_schema()
    print("Esquema OK")
