# main.py
# Programa principal: simula un día completo en el invernadero (Persona 3)

from invernadero import Invernadero
from zona import ZonaCultivo


def main():
    invernadero = Invernadero("Invernadero La Esperanza")

    # cada zona tiene sus propios límites: temp mínima, temp máxima,
    # humedad mínima del suelo y luz mínima
    zona_a = ZonaCultivo("Zona A", "Tomate", 18, 26, 50, 300)
    zona_b = ZonaCultivo("Zona B", "Lechuga", 15, 22, 60, 250)
    invernadero.agregar_zona(zona_a)
    invernadero.agregar_zona(zona_b)

    print("Simulando 24 horas (cada ciclo es una hora)")
    for hora in range(1, 25):
        invernadero.simular_hora()
        if hora % 6 == 0:          # reporte cada 6 horas para no llenar la pantalla
            print()
            print(invernadero.reporte())

    # el operario prueba el control manual (aquí se ve el manejo de errores)
    print("\nControl manual en la Zona A:")
    zona_a.accion_manual("ventilacion", True)
    zona_a.accion_manual("ventilacion", True)    # ya estaba encendida
    zona_a.accion_manual("ventilacion", False)
    zona_a.accion_manual("ventilacion", False)   # ya estaba apagada

    print("\nFin de la simulación")


if __name__ == "__main__":
    main()
