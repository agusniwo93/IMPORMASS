import re


def es_ruc_valido(ruc: str) -> bool:
    return bool(re.match(r"^(10|20)\d{9}$", ruc.strip()))


def es_dni_valido(dni: str) -> bool:
    return bool(re.match(r"^\d{8}$", dni.strip()))


def es_email_valido(email: str) -> bool:
    if not email:
        return True  # opcional
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()))


def es_numero_positivo(valor: str) -> bool:
    try:
        return float(valor) >= 0
    except (ValueError, TypeError):
        return False


def es_entero_positivo(valor: str) -> bool:
    try:
        return int(valor) >= 0
    except (ValueError, TypeError):
        return False
