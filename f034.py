"""Restaura una copia portátil de las ejecuciones entregadas sin sobrescribir otras."""
from pathlib import Path
import zipfile,sqlite3
root=Path(__file__).resolve().parents[1]
dest=root/'mlflow_evidencia';dest.mkdir(exist_ok=True)
if not (dest/'mlflow.db').exists():
    with zipfile.ZipFile(root/'evidencias/mlflow_bundle.zip') as z:z.extractall(dest)
with sqlite3.connect(dest/'mlflow.db') as db:
    db.execute("update experiments set artifact_location=? where experiment_id != '0'",((dest/'mlartifacts').as_uri(),))
    for run_id, in db.execute('select run_uuid from runs').fetchall():
        db.execute('update runs set artifact_uri=? where run_uuid=?',((dest/'mlartifacts'/run_id/'artifacts').as_uri(),run_id))
print('mlflow ui --backend-store-uri sqlite:///'+str(dest/'mlflow.db')+' --port 5000')
