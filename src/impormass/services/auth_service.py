import hashlib
from typing import Optional, Tuple
from ..db.connection import get_conn

ROLES_VALIDOS = ("admin", "vendedor", "almacenero")


def _hash(clave: str) -> str:
    return hashlib.sha256(clave.encode()).hexdigest()


def validar(usuario: str, clave: str) -> Tuple[bool, Optional[str]]:
    """Retorna (True, rol) si las credenciales son correctas, (False, None) si no."""
    usuario = usuario.strip()
    if not usuario or not clave:
        return False, None
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT clave, rol FROM usuarios WHERE usuario=? LIMIT 1",
            (usuario,)
        )
        row = cur.fetchone()
        if row is None:
            return False, None
        stored = row[0]
        rol = row[1] if len(row) > 1 else "vendedor"
        # Migración: si la clave almacenada no es hash sha256, compara plano y actualiza
        if len(stored) != 64:
            if stored == clave:
                conn.execute(
                    "UPDATE usuarios SET clave=? WHERE usuario=?",
                    (_hash(clave), usuario)
                )
                return True, rol
            return False, None
        if stored == _hash(clave):
            return True, rol
        return False, None


def registrar(usuario: str, clave: str, rol: str = "vendedor") -> bool:
    usuario = usuario.strip()
    clave = clave.strip()
    if not usuario or not clave:
        return False
    if len(clave) < 4:
        return False
    if rol not in ROLES_VALIDOS:
        rol = "vendedor"
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, clave, rol) VALUES (?, ?, ?)",
                (usuario, _hash(clave), rol)
            )
        return True
    except Exception:
        return False


def listar_usuarios():
    """Lista todos los usuarios con su rol (para panel admin)."""
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, usuario, rol FROM usuarios ORDER BY usuario"
        )
        return list(cur.fetchall())


def cambiar_rol(user_id: int, nuevo_rol: str):
    """Cambia el rol de un usuario."""
    if nuevo_rol not in ROLES_VALIDOS:
        return
    with get_conn() as conn:
        conn.execute(
            "UPDATE usuarios SET rol=? WHERE id=?",
            (nuevo_rol, user_id)
        )


def eliminar_usuario(user_id: int):
    """Elimina un usuario por ID."""
    with get_conn() as conn:
        conn.execute("DELETE FROM usuarios WHERE id=?", (user_id,))
