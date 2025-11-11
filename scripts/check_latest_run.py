import mlflow

mlflow.set_tracking_uri('http://mlflow:5000')
client = mlflow.tracking.MlflowClient()

runs = client.search_runs(
    experiment_ids=['1'],
    order_by=['start_time DESC'],
    max_results=1
)

if runs:
    run = runs[0]
    print('=' * 70)
    print(f'Run: {run.data.tags.get("mlflow.runName", "N/A")}')
    print(f'Run ID: {run.info.run_id}')
    print('=' * 70)
    print(f'\nPARAMETERS ({len(run.data.params)}):')
    for key, value in sorted(run.data.params.items()):
        print(f'  - {key}: {value}')
    
    print(f'\nMETRICS ({len(run.data.metrics)}):')
    for key, value in sorted(run.data.metrics.items()):
        print(f'  - {key}: {value}')
    print('=' * 70)

