from ..db.connection import get_conn

def validar(usuario: str, clave: str) -> bool:
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT 1 FROM usuarios WHERE usuario=? AND clave=? LIMIT 1",
            (usuario, clave)
        )
        return cur.fetchone() is not None

def registrar(usuario: str, clave: str) -> bool:
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, clave) VALUES (?, ?)",
                (usuario.strip(), clave.strip())
            )
        return True
    except Exception:
        return False
