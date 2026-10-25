# Historial de la Actividad 6

## 1.1.1 · 25 de octubre de 2026
- Corrige el pie público de Trello y añade actualización histórica fechada; conserva las cuatro capturas.
- Actualiza cobertura de rúbrica y coteja las páginas 3–10 del reporte existente.
- Corrige sólo el instalador del notebook: reemplaza una llamada de reinicio inexistente y detecta versiones cargadas distintas; conserva todas sus salidas originales.
- Ejecuta las 14 celdas en Colab, Python 3.13.16, sin errores finales; publica captura, registro y descarga. Tras el reinicio fue necesario pulsar Ejecutar todo: continuación automática pendiente.
- Documenta siete topics existentes sin cambiarlos y Google Docs con permiso de comentar por enlace, comprobado en incógnito; actualiza Entrega en Trello.
- Conserva las siete pruebas y el workflow. No aplica endurecimiento opcional porque la continuación automática sigue pendiente.
- No modifica el reporte, experimento original, semillas, partición, cifras ni advertencias.

## 1.1.0 · 24 de octubre de 2026
- Integra resumen ejecutivo, SMART de cinco filas, escenarios, referencias y cobertura de rúbrica en el reporte.
- Añade PR, fiabilidad, Brier, ΔAUC pareado, McNemar entre modelos y potencia normal aproximada del A/B simulado.
- Cuaderno con código visible y 14 celdas de código ejecutadas; métricas y predicciones coinciden con el experimento original.
- Añade pruebas pytest de métricas y Streamlit, workflow GitHub Actions y aviso académico.
- Conserva semillas, hiperparámetros, partición, script original y las limitaciones del caso.
- Actualiza el enlace al Google Docs 1.1.0; permisos y tablero se documentan en la verificación de mejoras.

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
