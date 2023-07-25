export PYTHONPATH=.:./sPhysNet-MT:$PYTHONPATH

# Prepare input MMFF geometry for prediction
python scripts/sphysnet-mt/step1_mmff_geometry.py --smiles_list $@

# Download pretrained models
MODEL_FOLDER="./data/models/exp_ultimate_freeSolv_13_RDrun_2022-05-20_100307__201005/exp_ultimate_freeSolv_13_active_ALL_2022-05-20_100309"
if [ ! -d "$MODEL_FOLDER" ]; then
    bash sPhysNet-MT/bash_scripts/download_models_and_extract.bash
fi

# Predict with sPhysNet-MT
python scripts/sphysnet-mt/step2_model_prediction.py --smiles_list $@
