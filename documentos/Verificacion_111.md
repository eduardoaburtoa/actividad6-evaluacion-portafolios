# Cierre de consistencia 1.1.1

25 de octubre de 2026. Conservo el reporte 1.1.0 y los resultados publicados; este cierre ajusta documentación, instalación y evidencia de acceso.

| Tarea | Estado real | Evidencia |
|---|---|---|
| 1. Visibilidad Trello | Resuelto | [PDF corregido](../tablero/Evidencia_Trello.pdf), [actualización histórica](Revision_2.md), [consulta pública](../evidencias/trello_publico110.png). Conservé las cuatro capturas. |
| 2. Cobertura de rúbrica | Resuelto | [Matriz actualizada](Cobertura_rubrica.md); cotejo página por página, sin cambiar cifras. |
| 3. Google Colab | Parcial | Ejecuté las 14 celdas, Python 3.13.16, cero errores en la ejecución final y tres corridas MLflow FINISHED. [Registro](../resultados/colab_110.json), [captura](../evidencias/colab_110.png), [cuaderno descargado](../evidencias/colab_ejecutado111.zip). El reinicio funciona, pero tuve que pulsar Ejecutar todo otra vez: continuación automática pendiente. |
| 4. Topics | Resuelto | [Captura About](../evidencias/topics_111.png): machine-learning, model-evaluation, mlflow, ab-testing, nlp, banking, tecmilenio; ya estaban publicados. |
| 5. Google Docs | Resuelto | [Permiso de comentar](../evidencias/google_docs_permiso111.png), [acceso en incógnito](../evidencias/google_docs_incognito111.png). README y tarjeta Entrega actualizados. |
| 6. Endurecimiento opcional | No aplicado | La instrucción condiciona esta tarea a cerrar las anteriores; conservo siete pruebas y CI sin cambios mientras queda pendiente la continuación automática. |

## Comprobación del reporte

Cotejé el PDF vigente: p. 3 decisión y SMART; p. 4 protocolo de datos y modelos; p. 5 matriz y escenarios (Tabla 4); p. 6 ROC/PR y fiabilidad (Figuras 2 y 3); p. 7 validación y significancia; p. 8 A/B; p. 9 impacto y conclusión; p. 10 referencias. No reescribí ni regeneré el reporte.

## Integridad y ejecución

El SHA-256 de `fuentes/experimento.py` sigue siendo `4084da16ebe2f67af618f78beab450d040aa968c418ce7d37e759fbe9d95a32f`. Comparé el notebook con el commit 047c086: sólo cambia el código de la primera celda; las salidas y los 14 contadores originales permanecen idénticos. La copia descargada de Colab tiene exactamente las mismas fuentes corregidas y contadores de 1 a 14, sin salidas de tipo error; se guarda aparte como evidencia.

El primer intento en Colab falló porque `google.colab.runtime.restart_runtime()` no existe. El instalador corregido reinició el proceso; después de reconectar pulsé Ejecutar todo. Las 14 celdas finalizaron. No presento esta secuencia como continuación automática. Los metadatos de ejecución históricos que Colab conserva en el JSON no se usan como fecha de la nueva sesión.

La meta conjunta sigue incumplida, el A/B es simulado, el test es retrospectivo, el 1 % + 1 % es un supuesto didáctico y los costos de error no son pesos. Una noticia negativa no es una orden de inversión.

## Comandos de comprobación

Desde la raíz, con las dependencias instaladas:

```bash
python fuentes/verificar.py
python fuentes/auditoria.py
python -m pytest pruebas -q
```

Para reproducir la ampliación sin cambiar el modelo, en una copia de trabajo:

```bash
python -m fuentes.ampliacion
```

Este último comando regenera artefactos locales. En este cierre no volví a entrenar localmente ni sustituí las cifras publicadas. La ejecución completa solicitada ocurrió en Colab. El resultado de las comprobaciones locales queda en [validacion_111.json](../resultados/validacion_111.json).
