# Protección de la integridad de la entrega

**Estado: propuesta de mejora; no integrada en main.**

Base: cierre 1.1.1, commit `fefe906`. Esta rama conserva la entrega y prepara una mejora independiente. Su integración requiere revisar los cambios y su evidencia.

## Objetivo
Quiero detectar cambios accidentales en las evidencias antes de incorporarlos a la entrega académica.

## Punto de partida
La entrega conserva siete pruebas aprobadas. El endurecimiento opcional se dejó pendiente en el cierre 1.1.1. Esta rama prepara su revisión independiente; no afirma que ya esté implementado.

## Trabajo previsto
- Añadir una prueba que compruebe 14 celdas de código, sus contadores de ejecución y ausencia de salidas de error.
- Comprobar la conservación de las salidas originales frente a la versión de referencia.
- Evaluar la regeneración y contraste de la ampliación estadística en CI sin sustituir las cifras publicadas.
- Medir la duración del workflow antes de proponer su integración.

## Criterios para integrar
- Pasan las siete pruebas actuales y las nuevas verificaciones.
- Una copia de prueba con salidas borradas o con un error es rechazada.
- El SHA-256 del experimento original permanece intacto.
- La ampliación conserva las tolerancias numéricas y se ejecuta en una copia temporal.
- No se afirma cumplir el límite de dos minutos sin medirlo.

## Evidencia de referencia
[Pruebas actuales](pruebas/test_metricas.py) · [Validación 1.1.1](resultados/validacion_111.json)
