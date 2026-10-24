"""Segunda revisión reproducible: evidencia, métricas, modelos, CV y A/B.
No vuelve a elegir modelos o umbrales mirando el test.
"""
from pathlib import Path
import json,hashlib,re,zipfile
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,average_precision_score,confusion_matrix
from scipy.stats import fisher_exact,binomtest
R=Path(__file__).resolve().parents[1]

def main():
 checks=[]
 def check(value,label):
  if not bool(value):raise ValueError(label)
  checks.append(label)
 d=pd.read_csv(R/'datos/datos_limp/phrasebank_v1.csv');manifest=json.loads((R/'datos/manifest.json').read_text())
 check(hashlib.sha256((R/'datos/datos_limp/phrasebank_v1.csv').read_bytes()).hexdigest()==manifest['clean_sha256'],'Hash del dataset limpio')
 check(hashlib.sha256((R/'datos/datos_ini/Sentences_AllAgree.txt').read_bytes()).hexdigest()==manifest['original_sha256'],'Hash del dataset original')
 check(len(d)==2259 and d.id.is_unique and not d.texto.isna().any(),'Integridad de 2259 registros')
 check(not d.texto.str.casefold().duplicated().any(),'Textos sin duplicados normalizados')
 dev=d[d.split=='train'];test=d[d.split=='test'];p=pd.read_csv(R/'resultados/predicciones_test.csv');m=pd.read_csv(R/'resultados/metricas_test.csv')
 check(list(p.id)==list(test.id) and len(p)==452,'Correspondencia exacta del test histórico')
 check(np.array_equal(p.y,(p.etiqueta=='negative').astype(int)),'Clase positiva correctamente codificada')
 for row in m.itertuples():
  score=p[row.model].to_numpy() if row.policy!='baseline' else (np.ones(len(p)) if row.model=='Revisar_todas' else np.full(len(p),(dev.etiqueta=='negative').mean()))
  pred=score>=row.threshold;cm=confusion_matrix(p.y,pred,labels=[0,1]).ravel();tn,fp,fn,tp=cm
  values=dict(accuracy=accuracy_score(p.y,pred),precision=precision_score(p.y,pred,zero_division=0),recall=recall_score(p.y,pred),f1=f1_score(p.y,pred),auc=roc_auc_score(p.y,score),average_precision=average_precision_score(p.y,score),tn=tn,fp=fp,fn=fn,tp=tp,cost_per_100=100*(5*fn+fp)/len(p),review_rate=pred.mean())
  check(all(np.isclose(v,getattr(row,k),atol=1e-12) for k,v in values.items()),f'Métricas completas {row.model} {row.policy}')
 for name in ['Logistica','SVM_calibrada']:
  model=joblib.load(R/f'resultados/modelo_{name}.joblib')
  check(np.allclose(model.predict_proba(p.texto)[:,1],p[name],atol=1e-12),f'Modelo recargado {name}')
 cv=pd.read_csv(R/'resultados/predicciones_cv.csv');cvmetrics=pd.read_csv(R/'resultados/validacion_cruzada.csv')
 for name,g in cv.groupby('model'):
  check(len(g)==len(dev) and g.id.is_unique and set(g.id)==set(dev.id),f'Cada registro de desarrollo aparece una vez OOF {name}')
  check(set(g.fold)==set(range(5)) and set(g.id).isdisjoint(test.id),f'Cinco folds sin IDs del test {name}')
  for fold,part in g.groupby('fold'):
   row=cvmetrics[(cvmetrics.model==name)&(cvmetrics.fold==fold)].iloc[0];pred=part.score>=part.threshold
   check(np.isclose(f1_score(part.y,pred),row.f1) and np.isclose(roc_auc_score(part.y,part.score),row.auc),f'Métricas OOF {name} fold {fold}')
 a=pd.read_csv(R/'resultados/ab_simulado.csv');ab=json.loads((R/'resultados/ab_analisis.json').read_text())
 check(len(a)==150 and a.cliente_id.is_unique and a.posicion_mxn.between(5e6,20e6).all(),'150 clientes ficticios únicos de 5 a 20 millones')
 A=a[a.grupo=='A'].exito_revision_simulado;B=a[a.grupo=='B'].exito_revision_simulado
 check(len(A)==75 and len(B)==75 and A.sum()==ab['successA'] and B.sum()==ab['successB'],'Conteos A/B')
 check(np.isclose(fisher_exact([[A.sum(),75-A.sum()],[B.sum(),75-B.sum()]]).pvalue,ab['fisher_exact_p']),'Fisher recalculado')
 stats=json.loads((R/'resultados/estadistica.json').read_text());b,c=stats['mcnemar_discordant']
 check(np.isclose(binomtest(b,b+c,.5).pvalue,stats['mcnemar_exact_p']),'McNemar recalculado')
 runs=json.loads((R/'evidencias/mlflow_runs.json').read_text());byid={x['run_id']:x for x in runs}
 for run in json.loads((R/'resultados/entorno.json').read_text())['runs']:
  row=m[(m.model==run['model'])&(m.policy=='ajustado')].iloc[0];record=byid[run['run_id']]
  check(record['status']=='FINISHED' and all(np.isclose(record['metrics'][k],row[k]) for k in ['accuracy','precision','recall','f1','auc']),f'MLflow coincide con CSV {run["model"]}')
  check(record['params']['code_sha256']==hashlib.sha256((R/'fuentes/experimento.py').read_bytes()).hexdigest(),f'Código coincide con ejecución {run["model"]}')
 with zipfile.ZipFile(R/'evidencias/mlflow_bundle.zip') as z:check(z.testzip() is None and 'mlflow.db' in z.namelist(),'Paquete MLflow íntegro')
 for target in re.findall(r'\]\(([^)]+)\)',(R/'README.md').read_text()):
  if not target.startswith(('http:','https:','#')):check((R/target.split("#",1)[0]).exists(),f'Enlace interno {target}')
 for target in ['documentos/Actividad6_Eduardo_Aburto.pdf','tablero/Evidencia_Trello.pdf','evidencias/Evidencia_MLflow.pdf']:
  check((R/target).read_bytes().startswith(b'%PDF'),'PDF presente '+target)
 result={'date':'2026-10-23','passed':len(checks),'checks':checks,'scope':'Comprueba artefactos y cálculos; no certifica rendimiento futuro ni calificación.'}
 (R/'resultados/auditoria_revision2.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(f'{len(checks)} comprobaciones correctas.')
if __name__=='__main__':main()
