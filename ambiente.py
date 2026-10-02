# ambiente.py
# Las condiciones "reales" de una zona
# Los sensores miden esto y más adelante los actuadores lo van a modificar.


class Ambiente:

    def __init__(self, temperatura=22, humedad_suelo=60, humedad_aire=65, hora=6):
        self.temperatura = temperatura
        self.humedad_suelo = humedad_suelo
        self.humedad_aire = humedad_aire
        self.hora = hora
        self.luz = self._luz_de_la_hora()

    def _luz_de_la_hora(self):
        # a las 12 hay más luz y baja hacia la mañana y la tarde
        return max(0, 900 - abs(12 - self.hora) * 140)

    def avanzar_hora(self):
        self.hora = (self.hora + 1) % 24
        self.luz = self._luz_de_la_hora()
        # la temperatura se acerca a la de afuera (más luz, más calor)
        afuera = 14 + self.luz / 60
        self.temperatura += (afuera - self.temperatura) * 0.3
        # el suelo se seca y con calor el aire queda más seco
        self.humedad_suelo = max(0, self.humedad_suelo - 2)
        self.humedad_aire = 90 - self.temperatura
