"""Análisis adicional retrospectivo; no altera modelos, semillas ni particiones."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, brier_score_loss, precision_recall_curve, average_precision_score, roc_curve
from sklearn.calibration import calibration_curve
from scipy.stats import binomtest, norm
from scipy.optimize import brentq
from fuentes.experimento import measure
ROOT=Path(__file__).resolve().parents[1]

def power(delta,n=75,p1=.72):
    # Aproximación normal bilateral con varianzas bajo H0 y H1.
    p2=p1+delta;bar=(p1+p2)/2
    crit=norm.ppf(.975)*np.sqrt(2*bar*(1-bar)/n)
    se=np.sqrt((p1*(1-p1)+p2*(1-p2))/n)
    return float(norm.sf((crit-delta)/se)+norm.cdf((-crit-delta)/se))

def main():
    out=ROOT/'resultados';d=pd.read_csv(out/'predicciones_test.csv')
    y=d.y.to_numpy();s=d.SVM_calibrada.to_numpy();l=d.Logistica.to_numpy()
    rng=np.random.default_rng(20261022);diff=[]
    for _ in range(2000):
        idx=np.concatenate([rng.choice(np.flatnonzero(y==k),sum(y==k),replace=True) for k in [0,1]])
        diff.append(roc_auc_score(y[idx],s[idx])-roc_auc_score(y[idx],l[idx]))
    ci=np.quantile(diff,[.025,.975]);a=((s>=.2)==y);b=((l>=.125)==y)
    only_s=int((a&~b).sum());only_l=int((b&~a).sum())
    # Cola empírica con corrección +1; no equivale a una prueba nula centrada.
    tail=float(min(1,2*(min(sum(np.array(diff)<=0),sum(np.array(diff)>=0))+1)/2001))
    result={'scope':'Exploratorio; test retrospectivo; sin ajuste por multiplicidad ni incertidumbre de reentrenamiento','seed':20261022,'bootstrap_repeats':2000,'delta_auc':float(roc_auc_score(y,s)-roc_auc_score(y,l)),'delta_auc_ci95':ci.tolist(),'bootstrap_two_sided_tail_plus1':tail,'bootstrap_tail_interpretation':'Proporción de cola empírica corregida; no p-valor de una distribución nula centrada.','mcnemar_models':{'svm_only_correct':only_s,'logistic_only_correct':only_l,'p':float(binomtest(only_s,only_s+only_l,.5).pvalue)},'brier':{'SVM':float(brier_score_loss(y,s)),'Logistica':float(brier_score_loss(y,l))},'mean_probability_svm':float(s.mean()),'prevalence':float(y.mean()),'ab_design':{'method':'Aproximación normal bilateral; pA=.72; n=75 por brazo; alpha=.05; no potencia exacta de Fisher','power_assumed_delta_0_13':power(.13),'mde_power_0_8':float(brentq(lambda delta:power(delta)-.8,.001,.279))}}
    (out/'ampliacion.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    scenarios=pd.DataFrame([{'threshold':t,**measure(y,s,t),'reviews':int((s>=t).sum())} for t in [.075,.2,.5]])
    scenarios.to_csv(out/'escenarios_umbral.csv',index=False)
    plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False,'font.size':10})
    fig,ax=plt.subplots(figsize=(7,3.3))
    for name,score,color in [('SVM calibrada',s,'#004481'),('Logística',l,'#49A5E6')]:
        prec,rec,_=precision_recall_curve(y,score);ax.plot(rec,prec,label=f'{name} AP={average_precision_score(y,score):.4f}',color=color)
    ax.axhline(y.mean(),ls='--',color='gray',label=f'Prevalencia {y.mean():.4f}');ax.set(xlabel='Recall',ylabel='Precisión',title='Precisión recall · test retrospectivo',ylim=(0,1.04));ax.legend();fig.tight_layout();fig.savefig(out/'precision_recall.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(6.5,3.1))
    for name,score,color in [('SVM calibrada',s,'#004481'),('Logística',l,'#49A5E6')]:
        actual,pred=calibration_curve(y,score,n_bins=8,strategy='quantile');ax.plot(pred,actual,'o-',label=name,color=color)
    ax.plot([0,1],[0,1],'--',color='gray',label='Referencia ideal');ax.set(xlabel='Probabilidad media por bin',ylabel='Fracción negativa observada',title='Fiabilidad · 8 bins de igual frecuencia');ax.legend();fig.tight_layout();fig.savefig(out/'fiabilidad.png',dpi=160);plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(10,3.3))
    for name,score,color in [('SVM',s,'#004481'),('Logística',l,'#49A5E6')]:
        fp,tp,_=roc_curve(y,score);axs[0].plot(fp,tp,label=f'{name} AUC={roc_auc_score(y,score):.4f}',color=color)
        prec,rec,_=precision_recall_curve(y,score);axs[1].plot(rec,prec,label=f'{name} AP={average_precision_score(y,score):.4f}',color=color)
    axs[0].plot([0,1],[0,1],'--',color='gray');axs[1].axhline(y.mean(),ls='--',color='gray',label='Prevalencia 0.1350')
    axs[0].set(xlabel='Tasa de falsos positivos',ylabel='Recall',title='ROC');axs[1].set(xlabel='Recall',ylabel='Precisión',title='Precisión recall')
    for ax in axs:ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'roc_pr.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,3));ax.hist(diff,bins=35,color='#1464A5');ax.axvline(0,color='gray',ls='--');ax.axvline(ci[0],color='#002E5D');ax.axvline(ci[1],color='#002E5D');ax.set(xlabel='AUC SVM menos AUC logística',ylabel='Remuestreos',title='Bootstrap pareado · 2,000 repeticiones');fig.tight_layout();fig.savefig(out/'delta_auc.png',dpi=160);plt.close(fig)
    m=pd.read_csv(out/'metricas_test.csv');cols=['model','policy','precision','recall','f1','auc']
    fig,ax=plt.subplots(figsize=(10,2.6));ax.axis('off');values=m[cols].copy()
    for c in cols[2:]:values[c]=values[c].map(lambda x:f'{x:.4f}')
    t=ax.table(cellText=values.values,colLabels=cols,loc='center',cellLoc='center');t.auto_set_font_size(False);t.set_fontsize(9);t.scale(1,1.7)
    for (row,col),cell in t.get_celld().items():
        if row==0:cell.set_facecolor('#004481');cell.get_text().set_color('white')
    fig.tight_layout();fig.savefig(out/'tabla_metricas.png',dpi=160);plt.close(fig)
    print(json.dumps(result,indent=2));print(scenarios.to_string(index=False))
if __name__=='__main__':main()
