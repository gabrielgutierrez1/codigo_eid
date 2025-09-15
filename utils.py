# utils.py
# Módulo con funciones de ayuda y validación.

def validar_funcion(expr_str):
    """Lanza un error si el string de la función está vacío."""
    if not expr_str.strip():
        raise ValueError("El campo de la función no puede estar vacío.")
    return expr_str

def validar_valor(valor_str):
    """
    Verifica si el string de un valor puede ser convertido a número.
    Devuelve un string vacío si la entrada está vacía.
    """
    if not valor_str.strip():
        return ""
    try:
        float(valor_str)
        return valor_str
    except ValueError:
        raise ValueError("El valor de 'x' para evaluar debe ser un número.")
