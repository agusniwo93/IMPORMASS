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
"""

def init_schema():
    with get_conn() as conn:
        conn.executescript(DDL)

if __name__ == "__main__":
    init_schema()
    print("Esquema OK")
