# excepciones.py
# Errores propios del invernadero


class LecturaInvalidaError(Exception):
    """Un sensor dio un valor imposible."""  
    pass


class ActuadorError(Exception):
    """Se le pidió a un actuador una acción inválida."""  
    pass