"""Análisis secundario retrospectivo; no modifica selección ni umbrales."""
from pathlib import Path
import json
import numpy as np,pandas as pd
from sklearn.metrics import roc_auc_score,f1_score
from scipy.stats import binomtest
R=Path(__file__).resolve().parents[1]
def main():
 p=pd.read_csv(R/'resultados/predicciones_test.csv');y=p.y.to_numpy();sv=p.SVM_calibrada.to_numpy();lr=p.Logistica.to_numpy()
 ps=sv>=.2;pl=lr>=.125;rng=np.random.default_rng(20261023);rows=[]
 for _ in range(5000):
  ix=np.concatenate([rng.choice(np.flatnonzero(y==k),sum(y==k),replace=True) for k in [0,1]])
  rows.append([roc_auc_score(y[ix],sv[ix])-roc_auc_score(y[ix],lr[ix]),f1_score(y[ix],ps[ix])-f1_score(y[ix],pl[ix])])
 ci=np.quantile(rows,[.025,.975],axis=0);b=int(((ps==y)&(pl!=y)).sum());c=int(((ps!=y)&(pl==y)).sum())
 out=dict(scope='Análisis secundario exploratorio del test histórico; sin corrección por multiplicidad. No prueba prospectiva ni fundamento nuevo para elegir modelo.',seed=20261023,repeats=5000,contrast='SVM 0.20 menos logística 0.125',delta_auc=roc_auc_score(y,sv)-roc_auc_score(y,lr),delta_auc_ci95=ci[:,0].tolist(),delta_f1=f1_score(y,ps)-f1_score(y,pl),delta_f1_ci95=ci[:,1].tolist(),mcnemar_discordant=[b,c],mcnemar_exact_p=binomtest(b,b+c,.5).pvalue)
 (R/'resultados/comparacion_pareada.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
