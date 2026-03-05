from typing import List, Tuple, Optional, Dict
from ..db.connection import get_conn


def _siguiente_numero(conn, serie: str = "F001") -> int:
    cur = conn.execute(
        "SELECT COALESCE(MAX(numero), 0) + 1 FROM facturas WHERE serie=?",
        (serie,),
    )
    return cur.fetchone()[0]


def crear(cliente_id: int, moneda: str, fecha_emision: str,
          subtotal: float, descuentos: float, valor_venta: float,
          igv: float, isc: float, icbper: float, otros_cargos: float,
          total: float, items: List[Dict], serie: str = "F001") -> Tuple[int, str]:
    """Crea factura con detalle. Retorna (factura_id, numero_formateado)."""
    with get_conn() as conn:
        numero = _siguiente_numero(conn, serie)
        cur = conn.execute(
            """INSERT INTO facturas
               (serie, numero, cliente_id, moneda, fecha_emision,
                subtotal, descuentos, valor_venta, igv, isc, icbper,
                otros_cargos, total)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (serie, numero, cliente_id, moneda, fecha_emision,
             subtotal, descuentos, valor_venta, igv, isc, icbper,
             otros_cargos, total),
        )
        factura_id = cur.lastrowid
        for it in items:
            conn.execute(
                """INSERT INTO factura_detalle
                   (factura_id, tipo, afectacion, unidad, cantidad, codigo,
                    descripcion, valor_unit, descuento, subtotal, igv, isc, icbper, total)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (factura_id, it["tipo"], it["afectacion"], it["unidad"],
                 it["cantidad"], it.get("codigo", ""), it["descripcion"],
                 it["valor_unit"], it.get("descuento", 0), it["subtotal"],
                 it.get("igv", 0), it.get("isc", 0), it.get("icbper", 0),
                 it["total"]),
            )
        num_formateado = f"{serie}-{numero:08d}"
        return factura_id, num_formateado


def listar(filtro: str = "") -> List[Tuple]:
    with get_conn() as conn:
        cur = conn.cursor()
        sql = """SELECT f.id, f.serie || '-' || printf('%08d', f.numero) AS num_factura,
                        c.razon_social, f.fecha_emision, f.moneda, f.total, f.estado
                 FROM facturas f
                 JOIN clientes c ON c.id = f.cliente_id"""
        if filtro:
            sql += " WHERE c.razon_social LIKE ? OR (f.serie || '-' || printf('%08d', f.numero)) LIKE ?"
            sql += " ORDER BY f.id DESC"
            cur.execute(sql, (f"%{filtro}%", f"%{filtro}%"))
        else:
            sql += " ORDER BY f.id DESC"
            cur.execute(sql)
        return list(cur.fetchall())


def obtener(factura_id: int) -> Optional[Tuple]:
    with get_conn() as conn:
        cur = conn.execute(
            """SELECT f.id, f.serie, f.numero, f.cliente_id, f.moneda,
                      f.fecha_emision, f.subtotal, f.descuentos, f.valor_venta,
                      f.igv, f.isc, f.icbper, f.otros_cargos, f.total, f.estado,
                      c.razon_social, c.num_doc, c.direccion
               FROM facturas f
               JOIN clientes c ON c.id = f.cliente_id
               WHERE f.id=?""",
            (factura_id,),
        )
        return cur.fetchone()


def obtener_detalle(factura_id: int) -> List[Tuple]:
    with get_conn() as conn:
        cur = conn.execute(
            """SELECT tipo, afectacion, unidad, cantidad, codigo,
                      descripcion, valor_unit, descuento, subtotal, igv, isc, icbper, total
               FROM factura_detalle WHERE factura_id=? ORDER BY id""",
            (factura_id,),
        )
        return list(cur.fetchall())


def anular(factura_id: int):
    with get_conn() as conn:
        conn.execute(
            "UPDATE facturas SET estado='ANULADA' WHERE id=?",
            (factura_id,),
        )
