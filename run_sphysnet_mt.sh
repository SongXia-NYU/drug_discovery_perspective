export PYTHONPATH=.:./sPhysNet-MT:$PYTHONPATH

# Prepare input MMFF geometry for prediction
python scripts/sphysnet-mt/step1_mmff_geometry.py

# Download pretrained models
bash sPhysNet-MT/bash_scripts/download_models_and_extract.bash

# Predict with sPhysNet-MT
python scripts/sphysnet-mt/step2_model_prediction.py
