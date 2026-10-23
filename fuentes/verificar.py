from pathlib import Path
import json,pandas as pd,numpy as np
from sklearn.metrics import confusion_matrix,recall_score,precision_score,roc_auc_score
r=Path(__file__).resolve().parents[1];p=pd.read_csv(r/'resultados/predicciones_test.csv');m=pd.read_csv(r/'resultados/metricas_test.csv')
for row in m[m.policy!='baseline'].itertuples():
    score=p[row.model];pred=score>=row.threshold
    assert np.isclose(recall_score(p.y,pred),row.recall)
    assert np.isclose(precision_score(p.y,pred),row.precision)
    assert np.isclose(roc_auc_score(p.y,score),row.auc)
    assert (confusion_matrix(p.y,pred).ravel()==[row.tn,row.fp,row.fn,row.tp]).all()
c=pd.read_csv(r/'contexto/clientes_simulados.csv');assert len(c)==150 and c.cliente_id.is_unique
assert c.posicion_mxn.between(5_000_000,20_000_000).all()
d=pd.read_csv(r/'datos/datos_limp/phrasebank_v1.csv');assert d.id.is_unique and set(d[d.split=='train'].id).isdisjoint(d[d.split=='test'].id)
a=pd.read_csv(r/'resultados/ab_simulado.csv');assert a.groupby('grupo').size().to_dict()=={'A':75,'B':75}
print('Verificación correcta: matrices, métricas, particiones y 150 clientes ficticios.')
