import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, ClassificationPreset
from pathlib import Path

# Simulation des métadonnées de la production et des données de référence
reference_data = pd.DataFrame({
    'image_width': [256] * 100,
    'image_height': [256] * 100,
    'brightness': [0.4, 0.5, 0.6] * 33 + [0.5],
    'target': [0, 1] * 50,
    'prediction': [0, 1, 0, 1] * 25
})

current_data = pd.DataFrame({
    'image_width': [256] * 50,
    'image_height': [256] * 50,
    'brightness': [0.1, 0.2, 0.15] * 16 + [0.2, 0.1],
    'target': [0, 1] * 25,
    'prediction': [0, 0, 1, 1] * 12 + [0, 1]
})

report = Report(metrics=[DataDriftPreset(), TargetDriftPreset(), ClassificationPreset()])
report.run(reference_data=reference_data, current_data=current_data)

output_dir = Path(__file__).resolve().parent
output_path = output_dir / "evidently_report.html"
output_dir.mkdir(parents=True, exist_ok=True)
report.save_html(output_path)

print(f"Rapport de monitoring Evidently généré avec succès dans : {output_path}")