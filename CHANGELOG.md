# Historial de la Actividad 6

## 1.0.1 · 23 de octubre de 2026
- Segunda revisión contra los cuatro criterios de la rúbrica; anexo `documentos/Revision_2.md`.
- Corrige incompatibilidad MLflow/SQLAlchemy detectada en instalación limpia; añade bloqueo completo de versiones.
- Reproduce entrenamiento y valida coincidencia de resultados; publica evidencia estructurada de la prueba.
- Añade auditoría de datos, modelos, métricas, folds, MLflow y enlaces.
- Agrega contraste pareado exploratorio SVM/logística; conserva resultados originales y sus límites.
- Hace repetible la celda inicial de Colab y protege rutas con espacios al restaurar MLflow.

## 1.0.0 · 22 de octubre de 2026
- Continúa la Actividad 5 (commit ffcab30094541ebbe7f52f1c55062068d59e1e4f).
- Conserva los datos y su partición histórica; transforma la etiqueta a negativa / no negativa.
- Implementa dos algoritmos, calibración dentro de folds, selección de umbral anidada, baselines y bootstrap pareado.
- Registra experimentos en MLflow; cambia el solver logístico a liblinear tras advertencias numéricas exploratorias. Se conservan las ejecuciones previas para auditoría; los IDs definitivos están en resultados/entorno.json.
- Incorpora A/B explícitamente simulado, Streamlit, reporte y tablero de evidencia.
- Actualiza índice público: 61 fichas DICI y 693 registros de comisiones por serie; extracción automática, requiere contrastar vigencia y periodicidad en la fuente.
