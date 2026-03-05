# src/impormass/services/config_service.py
"""Servicio para gestionar la configuración de la empresa y del sistema."""
from typing import Dict, Optional
from ..db.connection import get_conn

# Valores por defecto de la configuración
DEFAULTS = {
    # Datos de la empresa (emisor)
    "empresa_ruc": "",
    "empresa_razon_social": "",
    "empresa_nombre_comercial": "",
    "empresa_direccion": "",
    "empresa_departamento": "",
    "empresa_provincia": "",
    "empresa_distrito": "",
    "empresa_ubigeo": "",
    "empresa_telefono": "",
    "empresa_email": "",
    # Facturación
    "serie_factura": "F001",
    "serie_boleta": "B001",
    "igv_porcentaje": "18",
    "icbper_tarifa": "0.50",
    "moneda_defecto": "SOLES",
}


def obtener(clave: str) -> str:
    """Obtiene un valor de configuración. Retorna default si no existe."""
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT valor FROM configuracion WHERE clave=? LIMIT 1",
            (clave,)
        )
        row = cur.fetchone()
        if row is not None:
            return row[0]
        return DEFAULTS.get(clave, "")


def guardar(clave: str, valor: str):
    """Guarda o actualiza un valor de configuración."""
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT 1 FROM configuracion WHERE clave=? LIMIT 1", (clave,)
        )
        if cur.fetchone():
            conn.execute(
                "UPDATE configuracion SET valor=? WHERE clave=?",
                (valor, clave)
            )
        else:
            conn.execute(
                "INSERT INTO configuracion (clave, valor) VALUES (?, ?)",
                (clave, valor)
            )


def obtener_todo() -> Dict[str, str]:
    """Retorna toda la configuración como dict, incluyendo defaults."""
    result = dict(DEFAULTS)
    with get_conn() as conn:
        cur = conn.execute("SELECT clave, valor FROM configuracion")
        for row in cur.fetchall():
            result[row[0]] = row[1]
    return result


def guardar_todo(datos: Dict[str, str]):
    """Guarda múltiples claves de configuración."""
    with get_conn() as conn:
        for clave, valor in datos.items():
            cur = conn.execute(
                "SELECT 1 FROM configuracion WHERE clave=? LIMIT 1", (clave,)
            )
            if cur.fetchone():
                conn.execute(
                    "UPDATE configuracion SET valor=? WHERE clave=?",
                    (valor, clave)
                )
            else:
                conn.execute(
                    "INSERT INTO configuracion (clave, valor) VALUES (?, ?)",
                    (clave, valor)
                )


def obtener_info_db() -> Dict[str, str]:
    """Retorna información sobre la base de datos."""
    import os
    from ..config import DB_PATH
    info = {}
    try:
        info["ruta"] = str(DB_PATH)
        info["tamaño"] = f"{os.path.getsize(DB_PATH) / 1024:.1f} KB"
    except Exception:
        info["ruta"] = "No disponible"
        info["tamaño"] = "—"

    with get_conn() as conn:
        for tabla in ("usuarios", "productos", "clientes", "facturas", "factura_detalle"):
            try:
                cur = conn.execute(f"SELECT COUNT(*) FROM {tabla}")
                info[f"registros_{tabla}"] = str(cur.fetchone()[0])
            except Exception:
                info[f"registros_{tabla}"] = "0"
    return info


def exportar_backup(ruta_destino: str) -> bool:
    """Copia la base de datos a la ruta destino."""
    import shutil
    from ..config import DB_PATH
    try:
        shutil.copy2(str(DB_PATH), ruta_destino)
        return True
    except Exception:
        return False
