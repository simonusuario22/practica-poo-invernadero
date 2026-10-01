# excepciones.py
# Errores propios del invernadero


class LecturaInvalidaError(Exception):
    """Un sensor dio un valor imposible."""   # Persona 1
    pass


class ActuadorError(Exception):
    """Se le pidió a un actuador una acción inválida."""   # Persona 2
    pass