# invernadero.py
# El invernadero completo: varias zonas y un reporte general (Persona 3)

from sensores import Sensor


class Invernadero:

    def __init__(self, nombre):
        self.nombre = nombre
        self._zonas = []     # las zonas se crean afuera y se agregan aquí

    def agregar_zona(self, zona):
        self._zonas.append(zona)

    def simular_hora(self):
        # cada zona vive su hora por separado
        for zona in self._zonas:
            zona.ciclo()

    def reporte(self):
        lineas = [f"===== Reporte de {self.nombre} ====="]
        agua = 0
        for zona in self._zonas:
            lineas.append(str(zona))
            agua += zona.litros_agua
        lineas.append(f"Zonas: {len(self._zonas)} | Sensores: {Sensor.total_creados()} "
                      f"| Agua usada: {agua} litros")
        return "\n".join(lineas)

    def __str__(self):
        return f"{self.nombre} (zonas: {len(self._zonas)})"


if __name__ == "__main__":
    # Prueba del avance 3:  python invernadero.py
    from zona import ZonaCultivo

    invernadero = Invernadero("Prueba")
    invernadero.agregar_zona(ZonaCultivo("Zona A", "Tomate", 18, 26, 50, 300))
    invernadero.simular_hora()
    print(invernadero)
    print(invernadero.reporte())
