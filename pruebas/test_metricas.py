"""Pruebas de consistencia; ninguna cambia modelos ni datos."""
from pathlib import Path
import json,hashlib
import pandas as pd
import numpy as np
import pytest
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix,brier_score_loss
R=Path(__file__).resolve().parents[1]
P=pd.read_csv(R/'resultados/predicciones_test.csv')
M=pd.read_csv(R/'resultados/metricas_test.csv')
@pytest.mark.parametrize('index',M.index[M.policy!='baseline'].tolist())
def test_metricas_publicadas(index):
    row=M.loc[index];s=P[row.model];pred=s>=row.threshold
    for name,func in [('accuracy',accuracy_score),('precision',precision_score),('recall',recall_score),('f1',f1_score)]:
        assert np.isclose(func(P.y,pred),row[name],atol=1e-12)
    assert np.isclose(roc_auc_score(P.y,s),row.auc,atol=1e-12)
    assert (confusion_matrix(P.y,pred).ravel()==row[['tn','fp','fn','tp']].to_numpy()).all()
def test_datos_clientes_y_asignacion():
    d=pd.read_csv(R/'datos/datos_limp/phrasebank_v1.csv');c=pd.read_csv(R/'contexto/clientes_simulados.csv');ab=pd.read_csv(R/'resultados/ab_simulado.csv')
    assert d.id.is_unique and len(d)==2259
    assert set(d[d.split=='train'].id).isdisjoint(d[d.split=='test'].id)
    assert len(c)==150 and c.cliente_id.is_unique and c.posicion_mxn.between(5_000_000,20_000_000).all()
    assert ab.groupby('grupo').size().to_dict()=={'A':75,'B':75}
def test_integridad_y_ampliacion():
    assert hashlib.sha256((R/'fuentes/experimento.py').read_bytes()).hexdigest()=='4084da16ebe2f67af618f78beab450d040aa968c418ce7d37e759fbe9d95a32f'
    a=json.loads((R/'resultados/ampliacion.json').read_text())
    assert np.isclose(brier_score_loss(P.y,P.SVM_calibrada),a['brier']['SVM'],atol=1e-12)
    assert a['delta_auc_ci95'][0]>0
    scenarios=pd.read_csv(R/'resultados/escenarios_umbral.csv')
    for row in scenarios.itertuples():
        pred=P.SVM_calibrada>=row.threshold
        assert pred.sum()==row.reviews
        assert np.isclose(recall_score(P.y,pred),row.recall)
