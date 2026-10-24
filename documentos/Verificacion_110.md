# Verificación de mejoras 1.1.0

Fecha: 24 de octubre de 2026. Los estados distinguen archivos terminados de acciones externas pendientes. El reporte conserva el corte original del 22 de octubre y el trabajo de revisión iniciado el 23.

| Brecha | Estado | Evidencia |
|---|---|---|
| A1 Referencias APA 7 | resuelto | Reporte p. 10 y Referencias.md; autoría del artículo contrastada con fuente oficial. |
| A2 Figuras y tablas | resuelto | Cuatro figuras y ocho tablas numeradas con títulos y referencias en texto. |
| A3 Resumen ejecutivo | resuelto | Reporte p. 3, menos de 120 palabras. |
| A4 SMART | resuelto | Tabla 1, cinco filas y fecha de corte. |
| A5 Escenarios | resuelto | Tabla 4 y resultados/escenarios_umbral.csv. |
| A6 Significancia entre modelos | resuelto | Reporte p. 7, ampliacion.py y ampliacion.json. |
| A7 Calibración | resuelto | Brier y Figura 3; se evita afirmar calibración perfecta. |
| A8 PR | resuelto | Figura 2 y resultados/precision_recall.png. |
| A9 Potencia | resuelto | p. 8; aproximación 0.4911, MDE 17.84 puntos (17.9 redondeando hacia arriba); no se atribuye causalmente p a la muestra. |
| A10 CV vs A/B | resuelto | Tabla 7, cuatro dimensiones. |
| A11 Cobertura | resuelto | Tabla 8, cuatro criterios y frase solicitada. |
| A12 Voz personal | resuelto | Conclusión en primera persona, «ánimo», contexto bancario. |
| A13 Extensión | resuelto | Diez páginas totales: portada, declaración y ocho de contenido; revisión visual de todas las páginas. |
| A14 Identidad y declaración | resuelto | Plantilla azul, logotipo, matrícula, docente, fecha original; declaración de Codex y Claude. |
| B Cuaderno ejecutado | resuelto | fuentes/entrena.ipynb: 14 celdas de código ejecutadas, sin salidas de error; modelos, CV, umbrales, A/B y MLflow visibles. Ejecución local, no sesión Colab comprobada. |
| C1 Imágenes en Trello | resuelto | Matriz, métricas, ROC/PR, comparación, umbral y A/B adjuntos; portadas verificadas. |
| C2 Comparación en Trello | resuelto | Nueva tarjeta publicada con CV, ΔAUC y dos gráficas. |
| C3 Etiquetas y leyenda | resuelto | Verde, amarillo y rojo con tarjeta de leyenda publicada. |
| C4 Checklist de decisión | resuelto | Cinco criterios: cuatro documentados y validación externa pendiente. |
| C5 Público y capturas | parcial | PDF regenerado con capturas reales. Trello conserva acceso del espacio de trabajo; cambio público pendiente de confirmación directa tras rechazo automático. |
| D1 Pruebas | resuelto | pruebas/test_app.py y pruebas/test_metricas.py; siete pruebas pasaron localmente. |
| D2 CI | resuelto | GitHub Actions en Ubuntu: run 40104739285 completado con éxito; resultados/ci_110.json. |
| D3 Google Docs | resuelto | Nueva versión importada, acceso restringido indicado explícitamente en README; no se afirma acceso anónimo. |
| D4 Aviso | resuelto | AVISO.md. |
| D5 About y topics | resuelto | Descripción y siete topics publicados y comprobados. |
| D6 README | resuelto | Nuevos resultados y escenarios; auditoría Linux atribuida al autor, sin afirmar comprobación propia sin logs. |
| D7 CHANGELOG | resuelto | Versión 1.1.0. |
| D8 Figuras versionadas | resuelto | Todas bajo resultados/. |

## Integridad

No se cambió `fuentes/experimento.py`, sus hiperparámetros, semilla ni partición. Las métricas, predicciones y CV producidas por el cuaderno coinciden con los CSV originales con tolerancia 1e-12. El bootstrap adicional de 2,000 repeticiones usa semilla 20261022; se distingue del análisis previo de 5,000 repeticiones con semilla 20261023. Ambos quedan trazados.

La afirmación externa sobre Linux/Python 3.13/scikit-learn 1.9.1/MLflow 3.17.2 procede de las instrucciones aportadas por el autor; no hay logs adjuntos que permitan certificarla aquí. La prueba propia es macOS ARM/Python 3.12.14. La potencia es una aproximación normal bajo supuestos, no potencia exacta de Fisher. Un Brier favorable no acredita calibración perfecta.

## Comandos de comprobación

Desde la raíz del repositorio:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python fuentes/verificar.py
python fuentes/auditoria.py
python -m pytest pruebas -q
python -m fuentes.ampliacion
```

En Windows, activar con `.venv\Scripts\activate`. Para reentrenar: `python fuentes/experimento.py` (regenera resultados y MLflow locales). El notebook incorpora su instalación y sus instrucciones de reinicio cuando detecta versiones cargadas distintas.
