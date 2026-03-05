from typing import List, Tuple, Optional
from ..db.connection import get_conn

Row = Tuple  # id, tipo_doc, num_doc, razon_social, direccion, telefono, email


def listar(filtro: str = "") -> List[Row]:
    with get_conn() as conn:
        cur = conn.cursor()
        if filtro:
            cur.execute(
                """SELECT id, tipo_doc, num_doc, razon_social, direccion, telefono, email
                   FROM clientes
                   WHERE razon_social LIKE ? OR num_doc LIKE ?
                   ORDER BY razon_social""",
                (f"%{filtro}%", f"%{filtro}%"),
            )
        else:
            cur.execute(
                """SELECT id, tipo_doc, num_doc, razon_social, direccion, telefono, email
                   FROM clientes ORDER BY razon_social"""
            )
        return list(cur.fetchall())


def buscar_por_documento(num_doc: str) -> Optional[Row]:
    with get_conn() as conn:
        cur = conn.execute(
            """SELECT id, tipo_doc, num_doc, razon_social, direccion, telefono, email
               FROM clientes WHERE num_doc=? LIMIT 1""",
            (num_doc.strip(),),
        )
        return cur.fetchone()


def obtener(cliente_id: int) -> Optional[Row]:
    with get_conn() as conn:
        cur = conn.execute(
            """SELECT id, tipo_doc, num_doc, razon_social, direccion, telefono, email
               FROM clientes WHERE id=? LIMIT 1""",
            (cliente_id,),
        )
        return cur.fetchone()


def crear(tipo_doc: str, num_doc: str, razon_social: str,
          direccion: str = "", telefono: str = "", email: str = "") -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO clientes (tipo_doc, num_doc, razon_social, direccion, telefono, email)
               VALUES (?,?,?,?,?,?)""",
            (tipo_doc, num_doc.strip(), razon_social.strip(),
             direccion.strip(), telefono.strip(), email.strip()),
        )
        return cur.lastrowid


def actualizar(cliente_id: int, tipo_doc: str, num_doc: str, razon_social: str,
               direccion: str, telefono: str, email: str):
    with get_conn() as conn:
        conn.execute(
            """UPDATE clientes SET tipo_doc=?, num_doc=?, razon_social=?,
               direccion=?, telefono=?, email=? WHERE id=?""",
            (tipo_doc, num_doc.strip(), razon_social.strip(),
             direccion.strip(), telefono.strip(), email.strip(), cliente_id),
        )


def eliminar(cliente_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
