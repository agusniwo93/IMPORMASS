import hashlib
from ..db.connection import get_conn


def _hash(clave: str) -> str:
    return hashlib.sha256(clave.encode()).hexdigest()


def validar(usuario: str, clave: str) -> bool:
    usuario = usuario.strip()
    if not usuario or not clave:
        return False
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT clave FROM usuarios WHERE usuario=? LIMIT 1",
            (usuario,)
        )
        row = cur.fetchone()
        if row is None:
            return False
        stored = row[0]
        # Migración: si la clave almacenada no es hash sha256, compara plano y actualiza
        if len(stored) != 64:
            if stored == clave:
                conn.execute(
                    "UPDATE usuarios SET clave=? WHERE usuario=?",
                    (_hash(clave), usuario)
                )
                return True
            return False
        return stored == _hash(clave)


def registrar(usuario: str, clave: str) -> bool:
    usuario = usuario.strip()
    clave = clave.strip()
    if not usuario or not clave:
        return False
    if len(clave) < 4:
        return False
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, clave) VALUES (?, ?)",
                (usuario, _hash(clave))
            )
        return True
    except Exception:
        return False
