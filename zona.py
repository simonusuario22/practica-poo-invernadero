# zona.py
# Zona de cultivo: junta sensores y actuadores y decide qué encender (Persona 2)

from ambiente import Ambiente
from sensores import SensorTemperatura, SensorHumedadSuelo, SensorHumedadAmbiente, SensorLuz
from actuadores import Riego, Ventilacion, Calefaccion, Iluminacion
from excepciones import LecturaInvalidaError, ActuadorError


class ZonaCultivo:

    def __init__(self, nombre, cultivo, temp_min, temp_max, suelo_min, luz_min):
        self.nombre = nombre
        self.cultivo = cultivo
        # límites propios de la zona, cada cultivo necesita cosas distintas
        self._temp_min = temp_min
        self._temp_max = temp_max
        self._suelo_min = suelo_min
        self._luz_min = luz_min

        # la zona crea sus propios sensores y actuadores (composición)
        self._ambiente = Ambiente()
        self._sensores = {
            "temperatura": SensorTemperatura(self._ambiente),
            "suelo": SensorHumedadSuelo(self._ambiente),
            "aire": SensorHumedadAmbiente(self._ambiente),
            "luz": SensorLuz(self._ambiente),
        }
        self._actuadores = {
            "riego": Riego(self._ambiente),
            "ventilacion": Ventilacion(self._ambiente),
            "calefaccion": Calefaccion(self._ambiente),
            "iluminacion": Iluminacion(self._ambiente),
        }

    def ciclo(self):
        """Pasa una hora: cambia el clima, se leen los sensores y se decide."""
        self._ambiente.avanzar_hora()

        # lo que está encendido hace efecto sobre el ambiente
        for actuador in self._actuadores.values():
            actuador.aplicar_efecto()

        # leer sensores; si uno falla se queda con su última lectura buena
        for sensor in self._sensores.values():
            try:
                sensor.leer()
            except LecturaInvalidaError as error:
                print(f"  [{self.nombre}] {error}")

        # sin lecturas completas no se toca nada (estado seguro)
        if any(s.lectura is None for s in self._sensores.values()):
            print(f"  [{self.nombre}] faltan lecturas, no se cambia ningún actuador")
            return
        self._decidir()

    def _decidir(self):
        temp = self._sensores["temperatura"].lectura
        suelo = self._sensores["suelo"].lectura
        luz = self._sensores["luz"].lectura

        # cada regla dice cuándo encender y cuándo apagar
        self._regular("ventilacion", temp > self._temp_max, temp <= self._temp_max)
        self._regular("calefaccion", temp < self._temp_min, temp >= self._temp_min)
        self._regular("riego", suelo < self._suelo_min, suelo >= self._suelo_min)
        # el LED apaga más arriba para que no se prenda y apague cada hora
        self._regular("iluminacion", luz < self._luz_min, luz > self._luz_min + 400)

    def _regular(self, nombre, encender, apagar):
        actuador = self._actuadores[nombre]
        if encender and not actuador.encendido:
            actuador.activar()
        elif apagar and actuador.encendido:
            actuador.desactivar()

    def accion_manual(self, nombre, encender):
        """El operario enciende o apaga un actuador a mano."""
        actuador = self._actuadores[nombre]
        try:
            if encender:
                actuador.activar()
            else:
                actuador.desactivar()
        except ActuadorError as error:
            print(f"  [{self.nombre}] No se pudo: {error}")
        else:
            print(f"  [{self.nombre}] Listo -> {actuador}")

    @property
    def litros_agua(self):
        # litros que ha gastado el riego de esta zona
        return self._actuadores["riego"].litros_usados

    def __str__(self):
        lecturas = ", ".join(str(s) for s in self._sensores.values())
        encendidos = ", ".join(a.NOMBRE for a in self._actuadores.values() if a.encendido)
        return (f"{self.nombre} ({self.cultivo}) {self._ambiente.hora:02d}:00 | "
                f"{lecturas} | Encendidos: {encendidos or 'ninguno'}")


if __name__ == "__main__":
    # Prueba del avance 2:  python zona.py
    zona = ZonaCultivo("Zona A", "Tomate", 18, 26, 50, 300)

    print("--- un día completo ---")
    for _ in range(24):
        zona.ciclo()
        print(zona)

    print("--- control manual ---")
    zona.accion_manual("riego", True)
    zona.accion_manual("riego", True)    # ya estaba encendido
    zona.accion_manual("riego", False)
    zona.accion_manual("riego", False)   # ya estaba apagado
