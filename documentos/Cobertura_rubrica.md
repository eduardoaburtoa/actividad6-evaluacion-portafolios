# Cobertura de la rúbrica Actividad 6

| Criterio | Evidencia | Interpretación o límite |
|---|---|---|
| Problema, contexto y objetivo SMART | Reporte p. 3; README | Meta conjunta pendiente; escenarios distinguen recall de precisión |
| Matriz de confusión e interpretación | Reporte p. 5; resultados/confusion.png | TN 366, FP 25, FN 10, TP 51 |
| Accuracy, precisión, recall y F1 | Reporte pp. 5–7; resultados/metricas_test.csv; resultados/ampliacion.json; Figura 3, resultados/fiabilidad.png | Fórmulas y denominadores explícitos; Brier SVM 0.0463 frente a logística 0.0740, indicio favorable que no acredita calibración perfecta |
| Ajuste de umbral | Reporte p. 5, Tabla 4; resultados/umbrales_SVM_calibrada_desarrollo.csv; resultados/escenarios_umbral.csv | Tres escenarios 0.075 / 0.20 / 0.50; selección exclusivamente en desarrollo y meta conjunta no alcanzada |
| ROC y AUC | Reporte p. 6, Figura 2; resultados/roc_pr.png; resultados/precision_recall.png y CSV de curvas | AUC no es exactitud ni garantía de retorno; AP SVM 0.8468 y línea base PR 0.1350 |
| Validación cruzada y baseline | Reporte p. 4 y 7; validacion_cruzada.csv | 5 folds externos; mayoría y revisar todo |
| Significancia y generalización | Reporte p. 7; resultados/estadistica.json; resultados/ampliacion.json; resultados/comparacion_pareada.json | ΔAUC 0.0319, IC95 % [0.0206, 0.0451] (bootstrap de 2,000); McNemar entre modelos 54 frente a 1, p≈3.1×10⁻¹⁵. Análisis exploratorios sobre el mismo test retrospectivo, sin corrección por multiplicidad. comparacion_pareada.json conserva el análisis previo de 5,000 remuestreos y su propio intervalo |
| A/B y distinción frente a CV | Reporte p. 8, Tabla 7 y Figura 4; resultados/ab_simulado.csv; resultados/ab_analisis.json; resultados/ampliacion.json | A/B simulado; p=0.0703, sin efecto causal real. Potencia aproximada 0.4911 y MDE 17.84 puntos (17.9 redondeando hacia arriba) |
| Impacto de negocio y justificación | Reporte p. 3 y 9; Streamlit | Cliente, perfil y costos antes que corretaje |
| Registro de experimentos | evidencias/Evidencia_MLflow.pdf; evidencias/mlflow_bundle.zip; [GitHub Actions 40104739285](https://github.com/eduardoaburtoa/actividad6-evaluacion-portafolios/actions/runs/40104739285); resultados/ci_110.json | Corridas y artefactos MLflow verificables; CI de métricas y Streamlit aprobado |
| Notebook o script | fuentes/entrena.ipynb y fuentes/experimento.py | 14 celdas de código ejecutadas con salidas reales conservadas; comprobación de Colab documentada por separado en Verificacion_111.md |
| Tablero Trello | https://trello.com/b/2TN8TJQ1; tablero/Evidencia_Trello.pdf; evidencias/trello_publico110.png | 18 tarjetas; público desde el 24 de octubre de 2026 y verificado sin sesión; capturas en PDF |
| Reporte y edición | documentos/Actividad6_Eduardo_Aburto.pdf y .docx; Google Docs en README | Diez páginas totales; ocho de contenido más portada y declaración |
| Streamlit adicional | app.py | Probado localmente, no se afirma despliegue Cloud |

Esta matriz documenta evidencias; la calificación corresponde al docente.

## Segunda revisión · 23 de octubre de 2026

[Cotejo explícito de los cuatro criterios de 25 %, correcciones y pruebas](Revision_2.md). Incluye comparación estadística adicional entre algoritmos y reproducción desde un entorno limpio.

## Versión 1.1.0

[Verificación detallada A1–A14, B, C1–C5 y D1–D8](Verificacion_110.md). La Tabla 8 del reporte agrupa las evidencias por los cuatro criterios de 25 %.

## Cierre de consistencia 1.1.1

Cotejé individualmente las páginas del PDF vigente: p. 3 decisión y SMART; p. 4 protocolo de datos y modelos; p. 5 matriz y Tabla 4; p. 6 ROC/PR y fiabilidad; p. 7 validación y significancia; p. 8 A/B; p. 9 impacto, conclusión y cobertura; p. 10 referencias. No se modificó el reporte. Véase [estado de las seis tareas](Verificacion_111.md).
