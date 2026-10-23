"""Tablero académico: resultados fijos y exploración explícita, sin órdenes de inversión."""
from pathlib import Path
import json
import pandas as pd
import streamlit as st
from sklearn.metrics import confusion_matrix,precision_score,recall_score,f1_score
R=Path(__file__).resolve().parent
st.set_page_config(page_title='Vértice AI · Actividad 6',page_icon='📊',layout='wide')
st.image(str(R/'documentos/vertice_logo.png'),width=180)
st.title('Evaluar antes de recomendar')
st.caption('Eduardo Aburto Angulo · Actividad 6 · Asistente de preparación de revisiones de portafolio')
st.info('Prototipo académico. Clasifica noticias financieras en inglés para priorizar revisión humana. No predice rendimientos ni ejecuta movimientos. Los clientes y el A/B son simulados.')
m=pd.read_csv(R/'resultados/metricas_test.csv');p=pd.read_csv(R/'resultados/predicciones_test.csv');s=json.loads((R/'resultados/estadistica.json').read_text());ab=json.loads((R/'resultados/ab_analisis.json').read_text())
row=m[(m.model==s['selected_by_nested_cv_cost'])&(m.policy=='ajustado')].iloc[0]
for col,(title,value) in zip(st.columns(4),[('Recall',row.recall),('Precisión',row.precision),('F1',row.f1),('ROC-AUC',row.auc)]):col.metric(title,f'{value:.3f}')
st.warning('Meta no alcanzada: recall ≥90 % y precisión ≥60 %. SVM calibrada con umbral 0.20 es candidata a investigación; necesita validación externa antes de un piloto operativo.')
tabs=st.tabs(['Resultados','Umbral y errores','Validación y A/B','Cartera didáctica','Fuentes y trazabilidad'])
with tabs[0]:
 st.subheader('Comparación que sí podemos sostener')
 st.write('Seleccioné SVM por menor costo medio en validación cruzada anidada: 5 unidades por omisión y 1 por falsa alerta. Son ponderaciones didácticas, no pérdidas monetarias.')
 st.dataframe(m,hide_index=True)
 st.image(str(R/'resultados/roc.png'))
 st.caption('Test histórico de 452 noticias ya utilizado en Actividad 5. Esta evaluación es retrospectiva; no acredita generalización a noticias mexicanas actuales.')
with tabs[1]:
 st.image(str(R/'resultados/confusion.png'))
 st.write('Con umbral 0.20, las omisiones bajan de 21 a 10 y las falsas alertas suben de 7 a 25. Se revisan 76 noticias frente a 47. El cambio requiere capacidad operativa.')
 st.image(str(R/'resultados/umbral.png'))
 st.subheader('Explorador posterior al experimento')
 t=st.slider('Umbral ilustrativo sobre test (no cambia el modelo publicado)',0.05,0.95,0.20,0.025)
 pred=p.SVM_calibrada>=t
 st.json({'precision':round(precision_score(p.y,pred,zero_division=0),4),'recall':round(recall_score(p.y,pred),4),'f1':round(f1_score(p.y,pred),4),'matriz_TN_FP_FN_TP':confusion_matrix(p.y,pred).ravel().tolist()})
 st.caption('No elegir un nuevo umbral mirando este test. El umbral publicado se fijó con predicciones fuera de muestra del conjunto de desarrollo.')
with tabs[2]:
 st.dataframe(pd.read_csv(R/'resultados/validacion_cruzada.csv'),hide_index=True)
 st.write(f"AUC: IC bootstrap 95 % {s['auc_ci95'][0]:.3f}–{s['auc_ci95'][1]:.3f}. McNemar de exactitud: p={s['mcnemar_exact_p']:.4f}; no demuestra mejora de exactitud.")
 st.image(str(R/'resultados/ab.png'))
 st.write(f"A/B SIMULADO: 48/75 revisiones completas en A y 59/75 en B. Diferencia 14.67 puntos; Fisher bilateral p={ab['fisher_exact_p']:.4f}. No significativo al 5 %, y no constituye evidencia causal real.")
 st.caption('CV mide desempeño predictivo bajo remuestreo. A/B prospectivo mediría impacto del flujo de trabajo con asignación aleatoria. Son preguntas distintas.')
with tabs[3]:
 clients=pd.read_csv(R/'contexto/clientes_simulados.csv')
 st.write('150 superhéroes y villanos ficticios; posiciones entre $5 y $20 millones MXN. Los personajes permiten ilustrar perfiles sin usar información real. No entrenan el clasificador.')
 st.dataframe(clients[['cliente_id','nombre','perfil_riesgo','posicion_mxn']],hide_index=True)
 st.subheader('Punto de equilibrio de una migración hipotética')
 amount=st.number_input('Monto a migrar (MXN)',min_value=0.0,value=1000000.0,step=100000.0)
 excess=st.number_input('Mejora anual bruta supuesta (puntos porcentuales)',value=3.0,step=0.25)
 months=st.slider('Horizonte (meses)',1,36,12)
 cost=amount*.02;gross=amount*(excess/100)*(months/12)
 st.write(f'Corretaje didáctico: venta 1 % + compra 1 % sobre el mismo nocional = ${cost:,.0f}. Mejora bruta simple supuesta = ${gross:,.0f}. Saldo antes de impuestos, otros gastos y riesgo = ${gross-cost:,.0f}.')
 st.caption('Supuesto simplificado, no tarifa general verificada de BBVA. Sin garantía de rendimiento. No incluye variación de precios, capitalización ni diferencias de series. Si el rendimiento ya es neto de gastos del fondo, no se restan otra vez. El ingreso bancario no es equivalente al beneficio del cliente.')
with tabs[4]:
 st.write('Financial PhraseBank AllAgree, CC BY-NC-SA 3.0; uso académico. 2,264 originales y 2,259 tras deduplicar; 1,807 desarrollo y 452 test histórico.')
 st.dataframe(pd.read_csv(R/'contexto/comisiones_por_serie.csv'),hide_index=True)
 st.caption('61 fichas DICI públicas; 693 series extraídas automáticamente. Confirmar vigencia, periodicidad y elegibilidad en cada PDF; las fichas no forman parte del dataset NLP.')
 st.link_button('Normativa de fondos BBVA México','https://www.bbva.mx/personas/productos/inversion/normativa-de-fondos.html')
 st.json(json.loads((R/'resultados/entorno.json').read_text()))
 st.download_button('Descargar métricas', (R/'resultados/metricas_test.csv').read_bytes(),'metricas_test.csv','text/csv')
