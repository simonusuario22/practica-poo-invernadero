# Invernadero Inteligente

Práctica de Programación Orientada a Objetos (Python).
Simulamos un invernadero con varias zonas de cultivo. Cada zona tiene sensores que miden el ambiente y actuadores (riego, ventilación, calefacción y luz LED) que se encienden solos cuando algo se sale de los límites.

Integrantes: [Daniel Chaverra Rivera], [Simón Posada López]

## Cómo ejecutarlo

1. Tener Python 3 instalado (no hace falta instalar nada más, solo usamos librerías que ya vienen con Python).
2. Abrir la carpeta del proyecto en VS Code y abrir una terminal ahí.
3. Escribir:

```
python main.py
```

(En Windows, si `python` no funciona, probar con `py main.py`.)

## Qué hace el programa

Simula un día completo de 24 horas, donde cada ciclo es una hora. Hay dos zonas: una de tomate y una de lechuga, cada una con sus propios límites.

En cada hora pasa esto:

1. El clima cambia solo (de noche hace más frío y de día más calor y luz).
2. Los actuadores que estén encendidos modifican el ambiente.
3. Los sensores leen el ambiente.
4. La zona decide qué actuadores encender o apagar según sus límites.

Cada 6 horas se imprime un reporte con las lecturas de cada zona, qué está encendido y cuánta agua se ha usado. Al final se prueba el control manual, que muestra cómo se manejan los errores.

Los mensajes que dicen `dio -999, fuera del rango` son fallas de sensor que simulamos a propósito. El programa los atrapa, avisa y sigue usando la última lectura buena.

Cada archivo también se puede probar solo: `python sensores.py`, `python actuadores.py`, `python zona.py` o `python invernadero.py`.

## Archivos

| Archivo | Qué tiene |
|---|---|
| `main.py` | Programa principal, simula el día |
| `invernadero.py` | Clase `Invernadero`: guarda las zonas y hace el reporte |
| `zona.py` | Clase `ZonaCultivo`: sensores, actuadores y reglas de control |
| `sensores.py` | `Sensor` (abstracta) y 4 sensores hijos |
| `actuadores.py` | `Actuador` (abstracta) y 4 actuadores hijos |
| `ambiente.py` | Clase `Ambiente`: las condiciones reales de una zona |
| `excepciones.py` | Nuestras excepciones: `LecturaInvalidaError` y `ActuadorError` |

## Decisiones de diseño

- **Ambiente compartido.** En vez de inventar números al azar, cada zona tiene un objeto `Ambiente`. Los sensores miden eso (con un poco de ruido) y los actuadores lo modifican. Así, si se enciende la ventilación, la temperatura que lee el sensor baja de verdad.
- **Herencia.** `Sensor` y `Actuador` son clases abstractas. Lo que es igual para todos queda en la clase base y cada hijo solo escribe lo suyo (`_medir` en los sensores y `_modificar_ambiente` en los actuadores).
- **Zona con composición.** La zona crea sus propios sensores y actuadores. El invernadero solo recibe zonas ya hechas, por eso es una agregación.
- **Errores.** Si un sensor falla, la zona conserva la última lectura buena. Si faltan lecturas, no toca ningún actuador para dejar todo en un estado seguro.
- **Apagado con margen en la luz.** El LED se apaga con un límite más alto que el de encendido, para que no se prenda y apague cada hora.

## Dónde está cada tipo de método

| Tipo | Ejemplo en el código |
|---|---|
| Constructor | `Sensor.__init__`, `Actuador.__init__`, `ZonaCultivo.__init__` |
| De instancia | `leer()`, `activar()`, `desactivar()`, `ciclo()` |
| Estático | `Sensor.esta_en_rango()` |
| De clase | `Sensor.total_creados()` |
| Propiedad con setter | `Sensor.lectura` (valida el rango) |
| Método especial | `__str__` en sensores, actuadores, zona e invernadero |

## Cómo trabajamos

Usamos GitHub y repartimos el trabajo en 3 avances:

- Avance 1 : excepciones, ambiente y sensores.
- Avance 2 : actuadores y zona de cultivo.
- Avance 3 : invernadero, programa principal y este README.
