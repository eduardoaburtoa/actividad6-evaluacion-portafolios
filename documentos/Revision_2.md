# Segunda revisión de la Actividad 6

**Eduardo Aburto Angulo · 23 de octubre de 2026**

Contrasté la entrega con los cuatro criterios de la rúbrica original. Los cuatro cuentan con evidencia explícita. La revisión no asigna una calificación ni convierte el prototipo en una solución de inversión validada. Conservo la meta de recall incumplida: la rúbrica evalúa la calidad de la evaluación y su interpretación, no exige ocultar un resultado desfavorable.

## Cotejo de los cuatro criterios

| Criterio de la rúbrica | Evidencia comprobada | Conclusión de revisión |
|---|---|---|
| 1. Definición del problema, matriz y métricas (25 %) | Reporte páginas 3 y 5; matriz TP=51, FN=10, FP=25, TN=366; objetivo y costos de errores | Problema y clase positiva explícitos; métricas recalculadas y vinculadas a revisión humana. |
| 2. Matriz, métricas, ROC, AUC y umbral (25 %) | Reporte páginas 5–6; CSV de métricas y rejilla OOF; ROC | Cálculos consistentes. Umbral elegido en desarrollo; AUC distingue ordenamiento de exactitud y rentabilidad. |
| 3. Validación y comparación (25 %) | Reporte páginas 4 y 7–8; cinco folds externos, dos baselines, bootstrap, McNemar, Fisher y A/B | La CV y el A/B responden preguntas distintas. Test histórico y simulación declarados. Esta revisión añade comparación pareada entre algoritmos. |
| 4. Integración y presentación (25 %) | Justificación en reporte; portada, Streamlit, tablero Trello y PDF de capturas; evidencias MLflow | Decisión vinculada a omisiones, falsas alertas, carga de revisión, perfil y costos. Accesos organizados desde README. |

## Correcciones realizadas

1. **Dependencia de MLflow:** la instalación nueva resolvía SQLAlchemy 2.1.6. MLflow 2.22.2 no podía importar `FallbackAsyncAdaptedQueuePool` y fallaba antes de entrenar. Se fijó `SQLAlchemy==2.0.40`, compatible con la ejecución original. Se incluye `requirements-lock.txt` con el entorno completo comprobado.
2. **Notebook repetible:** la celda inicial reconoce si ya se encuentra en el proyecto y evita clonar una carpeta anidada al volver a ejecutarla. Se añadieron identificadores de celda.
3. **Restauración:** la instrucción de MLflow ahora protege rutas con espacios en terminales POSIX. En Windows se puede abrir el almacén usando comillas dobles en la ruta.
4. **Verificación ampliada:** `fuentes/auditoria.py` comprueba hashes, etiquetas, métricas completas y baselines, recarga de modelos, folds OOF, A/B, correspondencia MLflow, paquete ZIP y enlaces internos.

## Comparación estadística adicional

La comparación original de McNemar (p=0.2649) corresponde a **dos umbrales de la misma SVM**. No era una prueba entre SVM y regresión logística. Esta revisión agrega un análisis secundario retrospectivo entre las políticas ya fijadas: SVM 0.20 y logística 0.125, sin volver a elegir modelos o umbrales en el test.

Con 5,000 remuestreos estratificados pareados y semilla 20261023:

| Contraste SVM menos logística | Diferencia | IC percentil 95 % |
|---|---:|---:|
| AUC | 0.03186 | [0.01987, 0.04570] |
| F1 | 0.20286 | [0.15107, 0.25334] |

McNemar exacto de aciertos entre algoritmos: 54 casos correctos sólo con SVM y 1 sólo con logística; p=3.11×10⁻¹⁵. La evidencia condicional favorece a SVM en este test histórico. Es un análisis **exploratorio**, sin corrección por comparaciones múltiples y sin modelar la incertidumbre de reentrenamiento. No sustituye validación prospectiva, no demuestra rendimiento financiero y no convierte la comparación CV entre folds correlacionados en una prueba de muestras independientes.

El reporte de ocho páginas conserva la evaluación original del 22 de octubre. Este anexo fechado amplía la comparación entre algoritmos que allí se indicaba como no realizada. Los resultados originales no se alteraron.

## Pruebas de reproducción

Los detalles y resultados verificables se encuentran en [auditoria_revision2.json](../resultados/auditoria_revision2.json) y [reproduccion_revision2.json](../resultados/reproduccion_revision2.json). La instalación se probó en un entorno virtual nuevo, Python 3.12, CPU macOS ARM. La comprobación de otros sistemas operativos y versiones de Python queda fuera de este ensayo.

```bash
pip install -r requirements-lock.txt
python fuentes/auditoria.py
python fuentes/comparacion_pareada.py
```

Streamlit se probó al iniciar y al cambiar el umbral, el monto de migración y el horizonte. La aplicación permanece ejecutable localmente; no se afirma que tenga un despliegue activo en Streamlit Cloud. Trello conserva visibilidad del espacio de trabajo; las capturas PDF permiten revisar el tablero sin acceso a la cuenta.

## Límites que siguen vigentes

Recall de 83.6 % frente a meta de 90 %; corpus inglés histórico y licencia no comercial; A/B simulado, sin clientes reales; gastos y corretaje sujetos a los supuestos descritos. El siguiente paso de investigación es una validación temporal en español y un piloto supervisado, una vez resueltos datos, permisos y capacidad operativa.
