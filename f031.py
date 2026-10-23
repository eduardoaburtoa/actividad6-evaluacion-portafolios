"""Evaluación retrospectiva binaria, CV anidada de umbral y A/B SIMULADO."""
from pathlib import Path
import os,json,hashlib,time,platform,math
os.environ.setdefault('MPLBACKEND','Agg')
import numpy as np,pandas as pd,matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import StratifiedKFold,cross_val_predict
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,roc_curve,average_precision_score
from scipy.stats import fisher_exact,binomtest,norm
import mlflow
ROOT=Path(__file__).resolve().parents[1]
SEED=20261022
GRID=np.round(np.arange(.05,.951,.025),3)
COST_FN=5

def build(name):
    estimator=LogisticRegression(C=1,solver="liblinear",max_iter=3000,random_state=SEED) if name=='Logistica' else LinearSVC(C=1,dual='auto',max_iter=10000,random_state=SEED)
    pipe=make_pipeline(TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True,max_features=25000),estimator)
    return pipe if name=='Logistica' else CalibratedClassifierCV(pipe,method='sigmoid',cv=StratifiedKFold(3,shuffle=True,random_state=SEED),n_jobs=1)

def measure(y,p,t):
    pred=(np.asarray(p)>=t).astype(int)
    tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
    return {k:float(v) for k,v in dict(accuracy=accuracy_score(y,pred),precision=precision_score(y,pred,zero_division=0),recall=recall_score(y,pred,zero_division=0),f1=f1_score(y,pred,zero_division=0),auc=roc_auc_score(y,p),average_precision=average_precision_score(y,p),tn=tn,fp=fp,fn=fn,tp=tp,cost_per_100=100*(COST_FN*fn+fp)/len(y),review_rate=pred.mean()).items()}

def choose(y,p):
    rows=pd.DataFrame([dict(threshold=t,**measure(y,p,t)) for t in GRID])
    feasible=rows[(rows.recall>=.90)&(rows.precision>=.60)]
    pool=feasible if len(feasible) else rows
    winner=pool.sort_values(['cost_per_100','threshold'],ascending=[True,False]).iloc[0]
    return float(winner.threshold),bool(len(feasible)),rows

def wilson(k,n):
    z=norm.ppf(.9875);p=k/n;d=1+z*z/n
    c=(p+z*z/(2*n))/d;h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return float(c-h),float(c+h)

def ab_simulation(out):
    # Independent RNGs: assignment cannot change potential outcome generation.
    clients=pd.read_csv(ROOT/'contexto/clientes_simulados.csv')
    rng=np.random.default_rng(SEED);assigned=[]
    extra=0
    for _,group in clients.groupby('perfil_riesgo',sort=True):
        ids=rng.permutation(group.index)
        n_a=len(ids)//2+(len(ids)%2 and extra%2==0)
        if len(ids)%2:extra+=1
        assigned.extend((int(i),'A' if j<n_a else 'B') for j,i in enumerate(ids))
    arm=dict(assigned);sim=clients[['cliente_id','nombre','perfil_riesgo','posicion_mxn']].copy()
    sim['grupo']=[arm[i] for i in sim.index]
    rng=np.random.default_rng(SEED+1)
    sim['exito_revision_simulado']=(rng.random(len(sim))<np.where(sim.grupo=='A',.72,.85)).astype(int)
    sim['origen']='SIMULADO; no observaciones de clientes ni impacto financiero real'
    sim.to_csv(out/'ab_simulado.csv',index=False)
    a=sim[sim.grupo=='A'].exito_revision_simulado;b=sim[sim.grupo=='B'].exito_revision_simulado
    pa,pb=a.mean(),b.mean();la,ua=wilson(a.sum(),len(a));lb,ub=wilson(b.sum(),len(b))
    delta=pb-pa;ci=[lb-ua,ub-la]
    p=fisher_exact([[a.sum(),len(a)-a.sum()],[b.sum(),len(b)-b.sum()]]).pvalue
    p1,p2=.72,.85;avg=(p1+p2)/2
    n=math.ceil(((norm.ppf(.975)*np.sqrt(2*avg*(1-avg))+norm.ppf(.8)*np.sqrt(p1*(1-p1)+p2*(1-p2)))**2)/(p2-p1)**2)
    return dict(type='SIMULACION DIDACTICA',unit='cliente ficticio; una revisión por cliente',primary='proporción de revisiones completas en 48 h',hypotheses='H0: pB=pA; H1: pB!=pA',assumed_pA=p1,assumed_pB=p2,nA=len(a),nB=len(b),successA=int(a.sum()),successB=int(b.sum()),rateA=pa,rateB=pb,delta=delta,ci95_wilson_bonferroni_approx=ci,fisher_exact_p=p,alpha=.05,power_target=.8,approx_n_per_arm=n,n_with_10pct_loss=math.ceil(n/.9),interpretation='Demuestra el procedimiento, no prueba efecto causal real. El diseño final requiere evaluar contaminación entre asesores y efecto de agrupación.')

def main():
    out=ROOT/'resultados';out.mkdir(exist_ok=True)
    data=pd.read_csv(ROOT/'datos/datos_limp/phrasebank_v1.csv')
    data['y']=(data.etiqueta=='negative').astype(int)
    dev=data[data.split=='train'].reset_index(drop=True);test=data[data.split=='test'].reset_index(drop=True)
    X=dev.texto;y=dev.y;yt=test.y.to_numpy()
    # Every run uses a separate local store; original results can be preserved by copying the repo.
    mlflow.set_tracking_uri(f'sqlite:///{ROOT / "mlflow.db"}')
    exp='Actividad6_Evaluacion_'+str(SEED)
    # Reuse the store safely after moving the repository.
    import sqlite3
    if (ROOT/'mlflow.db').exists():
        with sqlite3.connect(ROOT/'mlflow.db') as db:
            if db.execute("select name from sqlite_master where name='experiments'").fetchone():
                db.execute('update experiments set artifact_location=? where name=?',((ROOT/'mlartifacts').as_uri(),exp))
    if mlflow.get_experiment_by_name(exp) is None:mlflow.create_experiment(exp,artifact_location=(ROOT/'mlartifacts').as_uri())
    mlflow.set_experiment(exp)
    folds=list(StratifiedKFold(5,shuffle=True,random_state=SEED).split(X,y))
    metrics=[];cvrows=[];thresholds={};probs={};oofall=[];runs=[]
    for name in ['Logistica','SVM_calibrada']:
        with mlflow.start_run(run_name=name) as run:
            start=time.perf_counter()
            for fold,(tr,va) in enumerate(folds):
                inner=StratifiedKFold(3,shuffle=True,random_state=SEED+fold)
                ptr=cross_val_predict(build(name),X.iloc[tr],y.iloc[tr],cv=inner,method='predict_proba',n_jobs=1)[:,1]
                t,feasible,_=choose(y.iloc[tr],ptr)
                m=build(name).fit(X.iloc[tr],y.iloc[tr]);pv=m.predict_proba(X.iloc[va])[:,1]
                cvrows.append(dict(model=name,fold=fold,threshold=t,feasible_inner=feasible,**measure(y.iloc[va],pv,t)))
                oofall.extend(dict(model=name,id=dev.iloc[j].id,fold=fold,y=int(y.iloc[j]),score=float(p),threshold=t) for j,p in zip(va,pv))
            # Fit final threshold only on development OOF predictions; no test target used.
            oof=cross_val_predict(build(name),X,y,cv=folds,method='predict_proba',n_jobs=1)[:,1]
            t,feasible,grid=choose(y,oof);thresholds[name]=dict(threshold=t,feasible_dev=feasible)
            grid.to_csv(out/f'umbrales_{name}_desarrollo.csv',index=False)
            model=build(name).fit(X,y);pt=model.predict_proba(test.texto)[:,1];probs[name]=pt
            for label,cut in [('default',.5),('ajustado',t)]:metrics.append(dict(model=name,policy=label,threshold=cut,**measure(yt,pt,cut)))
            mlflow.log_params(dict(seed=SEED,positive='negative',C=1,ngram='1,2',outer_folds=5,inner_threshold_folds=3,solver='liblinear' if name=='Logistica' else 'liblinear SVC',calibration='sigmoid 3 folds' if name!='Logistica' else 'none',threshold=t,cost_fn=COST_FN,cost_fp=1,source_commit='ffcab30094541ebbe7f52f1c55062068d59e1e4f',data_sha256=hashlib.sha256((ROOT/'datos/datos_limp/phrasebank_v1.csv').read_bytes()).hexdigest(),code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
            mlflow.log_metrics({**measure(yt,pt,t),'fit_seconds':time.perf_counter()-start})
            mlflow.log_artifact(str(out/f'umbrales_{name}_desarrollo.csv'))
            # Compact model for reproducible inference, own trusted artifact only.
            import joblib
            joblib.dump(model,out/f'modelo_{name}.joblib',compress=3)
            mlflow.log_artifact(str(out/f'modelo_{name}.joblib'))
            runs.append(dict(model=name,run_id=run.info.run_id))
    cv=pd.DataFrame(cvrows);cv.to_csv(out/'validacion_cruzada.csv',index=False)
    pd.DataFrame(oofall).to_csv(out/'predicciones_cv.csv',index=False)
    summary=cv.groupby('model')[['accuracy','precision','recall','f1','auc','cost_per_100']].agg(['mean','std'])
    summary.to_csv(out/'resumen_cv.csv')
    selected=cv.groupby('model').cost_per_100.mean().sort_values().index[0]
    for name,p,t in [('Dummy_mayoria',np.full(len(yt),y.mean()),.5),('Revisar_todas',np.ones(len(yt)),.5)]:metrics.append(dict(model=name,policy='baseline',threshold=t,**measure(yt,p,t)))
    pd.DataFrame(metrics).to_csv(out/'metricas_test.csv',index=False)
    pred=test[['id','texto','etiqueta','y']].copy()
    for name,p in probs.items():pred[name]=p
    pred.to_csv(out/'predicciones_test.csv',index=False)
    p=probs[selected];t=thresholds[selected]['threshold'];pp=(p>=t).astype(int);default=(p>=.5).astype(int)
    rng=np.random.default_rng(SEED);boot=[]
    for _ in range(2000):
        idx=np.concatenate([rng.choice(np.where(yt==k)[0],sum(yt==k),replace=True) for k in [0,1]])
        boot.append([roc_auc_score(yt[idx],p[idx]),f1_score(yt[idx],pp[idx]),recall_score(yt[idx],pp[idx])-recall_score(yt[idx],default[idx])])
    lo,hi=np.quantile(boot,[.025,.975],axis=0)
    b=int(((default==yt)&(pp!=yt)).sum());c=int(((default!=yt)&(pp==yt)).sum())
    stats=dict(selected_by_nested_cv_cost=selected,thresholds=thresholds,bootstrap_repeats=2000,auc_ci95=[lo[0],hi[0]],f1_ci95=[lo[1],hi[1]],delta_recall_ci95=[lo[2],hi[2]],mcnemar_discordant=[b,c],mcnemar_exact_p=float(binomtest(b,b+c,.5).pvalue) if b+c else 1,warning='Test histórico ya examinado en Actividad5; evaluación retrospectiva. IC condicionales al test, no prueba externa prospectiva.')
    ab=ab_simulation(out)
    (out/'estadistica.json').write_text(json.dumps(stats,indent=2,ensure_ascii=False))
    (out/'ab_analisis.json').write_text(json.dumps(ab,indent=2,ensure_ascii=False))
    (out/'entorno.json').write_text(json.dumps(dict(python=platform.python_version(),platform=platform.platform(),seed=SEED,mlflow=mlflow.__version__,runs=runs),indent=2))
    # Scientific figures, blue BBVA palette.
    plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False,'font.size':10})
    fig,ax=plt.subplots(figsize=(7,4))
    for name,score in probs.items():
        fpr,tpr,_=roc_curve(yt,score);ax.plot(fpr,tpr,label=f'{name} · AUC {roc_auc_score(yt,score):.3f}')
        pd.DataFrame(dict(fpr=fpr,tpr=tpr)).to_csv(out/f'roc_{name}.csv',index=False)
    ax.plot([0,1],[0,1],'--',color='gray',label='Azar · AUC 0.50');ax.set(xlabel='Tasa de falsos positivos',ylabel='Recall de noticias negativas',title='ROC · test histórico');ax.legend();fig.tight_layout();fig.savefig(out/'roc.png',dpi=160);plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(9,3.5))
    for ax,cut,label in zip(axs,[.5,t],['Umbral 0.50',f'Umbral {t:.3f}']):
        cm=confusion_matrix(yt,p>=cut);ax.imshow(cm,cmap='Blues')
        for i in range(2):
            for j in range(2):ax.text(j,i,str(cm[i,j]),ha='center',va='center',color='white' if cm[i,j]>cm.max()/2 else '#002E5D',fontsize=17)
        ax.set(xticks=[0,1],xticklabels=['No alerta','Alerta'],yticks=[0,1],yticklabels=['No negativa','Negativa'],xlabel='Predicción',ylabel='Real',title=label)
    fig.suptitle(selected+' · clase positiva = noticia negativa');fig.tight_layout();fig.savefig(out/'confusion.png',dpi=160);plt.close(fig)
    grid=pd.read_csv(out/f'umbrales_{selected}_desarrollo.csv');fig,ax=plt.subplots(figsize=(7,3.5))
    for col in ['precision','recall','f1']:ax.plot(grid.threshold,grid[col],label=col)
    ax.axvline(t,color='#004481',linestyle='--',label=f'elegido {t:.3f}');ax.set(xlabel='Umbral',ylabel='Métrica OOF',title='Ajuste en desarrollo · no se optimiza en test');ax.legend();fig.tight_layout();fig.savefig(out/'umbral.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,3.5));m=pd.DataFrame(metrics);m['label']=m.model+' '+m.policy
    m.set_index('label')[['recall','precision','f1']].plot.barh(ax=ax,color=['#004481','#1464A5','#49A5E6']);ax.set(xlim=(0,1),ylabel='',title='Test histórico · comparación con baselines');fig.tight_layout();fig.savefig(out/'comparacion.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(6,3));ax.bar(['A · manual','B · asistida'],[ab['rateA'],ab['rateB']],color=['#004481','#49A5E6']);ax.set(ylim=(0,1),ylabel='Revisiones completas / total',title='A/B SIMULADO · sin clientes reales');fig.tight_layout();fig.savefig(out/'ab.png',dpi=160);plt.close(fig)
    with mlflow.start_run(run_name='Validacion_y_AB_SIMULADO'):
        mlflow.log_params(dict(selected=selected,ab='SIMULADO',ab_seed=SEED,threshold=t));mlflow.log_metrics(dict(ab_fisher_p=ab['fisher_exact_p'],mcnemar_p=stats['mcnemar_exact_p']))
        for path in out.iterdir():
            if path.suffix in ['.json','.csv','.png']:mlflow.log_artifact(str(path))
    print(json.dumps(stats,indent=2));print(pd.DataFrame(metrics).to_string(index=False));print(json.dumps(ab,indent=2))
if __name__=='__main__':main()
