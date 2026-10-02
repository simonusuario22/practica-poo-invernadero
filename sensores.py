# sensores.py
# Sensores del invernadero

import random
from abc import ABC, abstractmethod

from excepciones import LecturaInvalidaError


class Sensor(ABC):
    NOMBRE = "Sensor"
    UNIDAD = ""
    RANGO = (0, 100)      # fuera de este rango la lectura es imposible

    _total = 0            # cuántos sensores se han creado

    def __init__(self, ambiente, prob_falla=0.03):
        Sensor._total += 1
        self._ambiente = ambiente
        self._prob_falla = prob_falla   # probabilidad de que el sensor falle
        self._lectura = None

    @property
    def lectura(self):
        return self._lectura

    @lectura.setter
    def lectura(self, valor):
        minimo, maximo = self.RANGO
        if not Sensor.esta_en_rango(valor, minimo, maximo):
            raise LecturaInvalidaError(f"{self.NOMBRE} dio {valor}, fuera del rango {self.RANGO}")
        self._lectura = valor

    @staticmethod
    def esta_en_rango(valor, minimo, maximo):
        return minimo <= valor <= maximo

    @classmethod
    def total_creados(cls):
        return cls._total

    def leer(self):
        if random.random() < self._prob_falla:
            self.lectura = -999   # falla simulada, el setter lo rechaza
        else:
            # el sensor se satura en los límites de su rango
            minimo, maximo = self.RANGO
            valor = min(maximo, max(minimo, self._medir()))
            self.lectura = round(valor, 1)
        return self._lectura

    @abstractmethod
    def _medir(self):
        pass

    def __str__(self):
        return f"{self.NOMBRE}: {self._lectura} {self.UNIDAD}"


class SensorTemperatura(Sensor):
    NOMBRE = "Temperatura"
    UNIDAD = "°C"
    RANGO = (-10, 60)

    def __init__(self, ambiente, prob_falla=0.03, sesgo=0):
        super().__init__(ambiente, prob_falla)
        self._sesgo = sesgo   # error de calibración del sensor

    def _medir(self):
        return self._ambiente.temperatura + self._sesgo + random.uniform(-0.4, 0.4)


class SensorHumedadSuelo(Sensor):
    NOMBRE = "Humedad del suelo"
    UNIDAD = "%"

    def _medir(self):
        return self._ambiente.humedad_suelo + random.uniform(-2, 2)


class SensorHumedadAmbiente(Sensor):
    NOMBRE = "Humedad del aire"
    UNIDAD = "%"

    def _medir(self):
        return self._ambiente.humedad_aire + random.uniform(-1.5, 1.5)


class SensorLuz(Sensor):
    NOMBRE = "Luminosidad"
    UNIDAD = "lux"
    RANGO = (0, 2000)

    def _medir(self):
        return self._ambiente.luz + random.uniform(-15, 15)


if __name__ == "__main__":
    # Prueba del avance 1:  python sensores.py
    from ambiente import Ambiente

    amb = Ambiente()
    sensores = [SensorTemperatura(amb, 0), SensorHumedadSuelo(amb, 0),
                SensorHumedadAmbiente(amb, 0), SensorLuz(amb, 0)]

    for _ in range(3):
        amb.avanzar_hora()
        print("Hora", amb.hora)
        for s in sensores:
            s.leer()
            print(s)

    print("Sensores creados:", Sensor.total_creados())

    # error 1: un sensor que siempre falla
    sensor_malo = SensorTemperatura(amb, prob_falla=1)
    try:
        sensor_malo.leer()
    except LecturaInvalidaError as error:
        print("Error controlado:", error)

    # error 2: asignar a mano una lectura imposible
    try:
        sensores[3].lectura = 5000
    except LecturaInvalidaError as error:
        print("Error controlado:", error)