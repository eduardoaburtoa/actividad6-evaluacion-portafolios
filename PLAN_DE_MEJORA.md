# Ejecución reproducible en Colab

**Estado: propuesta de mejora; no integrada en main.**

Base: cierre 1.1.1, commit `fefe906`. Esta rama conserva la entrega y prepara una mejora independiente. Su integración requiere revisar los cambios y su evidencia.

## Objetivo
Quiero simplificar el arranque del cuaderno para que un evaluador pueda reproducir la actividad con instrucciones claras y evidencia verificable.

## Punto de partida
La versión 1.1.1 ejecutó 14 celdas en Colab con cero errores finales. Tras reiniciar fue necesario pulsar «Ejecutar todo» de nuevo. La continuación automática sigue pendiente; esta rama todavía no la implementa.

## Trabajo previsto
- Evaluar una instalación aislada o un mecanismo compatible de continuación, sin cambiar el modelo.
- Probar una sesión nueva y otra con dependencias previamente cargadas.
- Conservar las salidas originales y guardar la nueva evidencia por separado.
- Documentar cualquier intervención que Colab siga requiriendo.

## Criterios para integrar
- Las 14 celdas terminan sin errores en una sesión Colab real.
- Las métricas coinciden con la entrega dentro de la tolerancia existente.
- El mecanismo de reinicio se prueba y describe sin afirmar automatización no comprobada.
- Se conservan el script original, semillas, hiperparámetros y partición.

## Evidencia de referencia
[Registro de Colab](resultados/colab_110.json) · [Verificación del cierre](documentos/Verificacion_111.md)
