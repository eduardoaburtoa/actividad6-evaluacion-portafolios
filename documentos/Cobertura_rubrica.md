# Cobertura de la rúbrica Actividad 6

| Criterio | Evidencia | Interpretación o límite |
|---|---|---|
| Problema, contexto y objetivo SMART | Reporte p. 3; README | Meta conjunta pendiente; escenarios distinguen recall de precisión |
| Matriz de confusión e interpretación | Reporte p. 5; resultados/confusion.png | TN 366, FP 25, FN 10, TP 51 |
| Accuracy, precisión, recall y F1 | Reporte p. 5 y 7; metricas_test.csv | Fórmulas y denominadores explícitos |
| Ajuste de umbral | Reporte p. 5; umbrales_SVM_calibrada_desarrollo.csv | Selección exclusivamente en desarrollo |
| ROC y AUC | Reporte p. 6; roc.png y CSV de curvas | AUC no es exactitud ni garantía de retorno |
| Validación cruzada y baseline | Reporte p. 4 y 7; validacion_cruzada.csv | 5 folds externos; mayoría y revisar todo |
| Significancia y generalización | Reporte p. 7; estadistica.json | Bootstrap y McNemar; test histórico retrospectivo |
| A/B y distinción frente a CV | Reporte p. 8; ab_simulado.csv y ab_analisis.json | Simulación; p=0.0703, no efecto causal real |
| Impacto de negocio y justificación | Reporte p. 3 y 9; Streamlit | Cliente, perfil y costos antes que corretaje |
| Registro de experimentos | evidencias/Evidencia_MLflow.pdf y mlflow_bundle.zip | Corridas y artefactos reales verificables |
| Notebook o script | fuentes/entrena.ipynb y experimento.py | Script y notebook ejecutados; 14 celdas de código con salidas reales |
| Tablero Trello | https://trello.com/b/2TN8TJQ1; tablero/Evidencia_Trello.pdf | Capturas permiten evaluar sin acceso a la cuenta |
| Reporte y edición | documentos/Actividad6_Eduardo_Aburto.pdf y .docx; Google Docs en README | Diez páginas totales; ocho de contenido más portada y declaración |
| Streamlit adicional | app.py | Probado localmente, no se afirma despliegue Cloud |

Esta matriz documenta evidencias; la calificación corresponde al docente.

## Segunda revisión · 23 de octubre de 2026

[Cotejo explícito de los cuatro criterios de 25 %, correcciones y pruebas](Revision_2.md). Incluye comparación estadística adicional entre algoritmos y reproducción desde un entorno limpio.

## Versión 1.1.0

[Verificación detallada A1–A14, B, C1–C5 y D1–D8](Verificacion_110.md). La Tabla 8 del reporte agrupa las evidencias por los cuatro criterios de 25 %.
