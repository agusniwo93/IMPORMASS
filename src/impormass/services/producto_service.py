from typing import List, Tuple
from ..db.connection import get_conn

Row = Tuple[str, str, float, int, str]  # codigo, nombre, precio, cantidad, descripcion

def listar(filtro: str = "") -> List[Row]:
    with get_conn() as conn:
        cur = conn.cursor()
        if filtro:
            cur.execute("""SELECT codigo,nombre,precio,cantidad,descripcion
                           FROM productos WHERE nombre LIKE ? ORDER BY nombre""",
                        (f"%{filtro}%",))
        else:
            cur.execute("""SELECT codigo,nombre,precio,cantidad,descripcion
                           FROM productos ORDER BY nombre""")
        return list(cur.fetchall())

def existe_codigo(codigo: str) -> bool:
    with get_conn() as conn:
        cur = conn.execute("SELECT 1 FROM productos WHERE codigo=? LIMIT 1", (codigo,))
        return cur.fetchone() is not None

def crear(nombre, codigo, precio, cantidad, descripcion=""):
    with get_conn() as conn:
        conn.execute("""INSERT INTO productos (nombre,codigo,precio,cantidad,descripcion)
                        VALUES (?,?,?,?,?)""",
                     (nombre, codigo, precio, cantidad, descripcion))

def actualizar(codigo, nombre, precio, cantidad, descripcion):
    with get_conn() as conn:
        conn.execute("""UPDATE productos
                        SET nombre=?, precio=?, cantidad=?, descripcion=?
                        WHERE codigo=?""",
                     (nombre, precio, cantidad, descripcion, codigo))

def eliminar(codigo: str):
    with get_conn() as conn:
        conn.execute("DELETE FROM productos WHERE codigo=?", (codigo,))
