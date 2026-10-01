# actuadores.py
# Actuadores del invernadero (Persona 2)

from abc import ABC, abstractmethod

from excepciones import ActuadorError


class Actuador(ABC):
    NOMBRE = "Actuador"

    def __init__(self, ambiente):
        self._ambiente = ambiente
        self._encendido = False

    @property
    def encendido(self):
        return self._encendido

    def activar(self):
        if self._encendido:
            raise ActuadorError(f"{self.NOMBRE} ya estaba encendido")
        self._encendido = True

    def desactivar(self):
        if not self._encendido:
            raise ActuadorError(f"{self.NOMBRE} ya estaba apagado")
        self._encendido = False

    def aplicar_efecto(self):
        # se llama cada hora; solo hace algo si está encendido
        if self._encendido:
            self._modificar_ambiente()

    @abstractmethod
    def _modificar_ambiente(self):
        pass

    def __str__(self):
        estado = "encendido" if self._encendido else "apagado"
        return f"{self.NOMBRE}: {estado}"


class Riego(Actuador):
    NOMBRE = "Riego"

    def __init__(self, ambiente):
        super().__init__(ambiente)
        self.litros_usados = 0

    def _modificar_ambiente(self):
        self._ambiente.humedad_suelo = min(100, self._ambiente.humedad_suelo + 15)
        self.litros_usados += 20   # cada hora de riego gasta 20 litros


class Ventilacion(Actuador):
    NOMBRE = "Ventilación"

    def _modificar_ambiente(self):
        self._ambiente.temperatura -= 2.5


class Calefaccion(Actuador):
    NOMBRE = "Calefacción"

    def _modificar_ambiente(self):
        self._ambiente.temperatura += 3


class Iluminacion(Actuador):
    NOMBRE = "Iluminación LED"

    def _modificar_ambiente(self):
        self._ambiente.luz += 400


if __name__ == "__main__":
    # Prueba del avance 2:  python actuadores.py
    from ambiente import Ambiente

    amb = Ambiente()
    ventilacion = Ventilacion(amb)
    print(ventilacion)

    ventilacion.activar()
    print(ventilacion, "| temperatura antes:", amb.temperatura)
    ventilacion.aplicar_efecto()
    print("temperatura después de una hora:", amb.temperatura)

    # error: activar un actuador que ya está encendido
    try:
        ventilacion.activar()
    except ActuadorError as error:
        print("Error controlado:", error)
    else:
        print("Se activó sin problema")
