"""
Make predictions using sPhysNet-MT
"""
from glob import glob
import os
import os.path as osp
import time
from typing import DefaultDict, Dict, List, Tuple, Union
import pandas as pd

from predict import EnsPredictor

tic = time.time()

# Trained sPhysNet-MT model on the calculated dataset. 
# The model can be used to predict DFT-level electronic energies.
model_paths_calc = "./data/models/exp_frag20sol_012_active_ALL_2022-05-01_112820/exp_*_cycle_-1_*"
# Trained model on the experimental dataset.
# The model can be used to predict experimental hydration free energy and logP.
model_paths_exp = "./data/models/exp_ultimate_freeSolv_13_RDrun_2022-05-20_100307__201005/exp_ultimate_freeSolv_13_active_ALL_2022-05-20_100309/exp_*_cycle_-1_*"

# records the model prediction on the drug molecules
pred_info: Dict[str, List[Union[str, float]]] = DefaultDict(lambda: [])
mmff_geometries: List[str] = glob("./data/mmff_geometries/conf_lowest/*.sdf")

for mmff_sdf in mmff_geometries:
    file_handle: str = osp.basename(mmff_sdf).split(".sdf")[0]
    pred_info["file_handle"].append(file_handle)

    # predict DFT level properties
    calc_predictor = EnsPredictor(model_paths_calc, mmff_sdf)
    pred, pred_std = calc_predictor.get_prediction()
    pred_info["E_gas(eV)"].append(pred["E_gas"])
    pred_info["E_water(eV)"].append(pred["E_water"])
    pred_info["E_oct(eV)"].append(pred["E_oct"])

    # predict experimental properties
    exp_predictor = EnsPredictor(model_paths_exp, mmff_sdf)
    pred, pred_std = calc_predictor.get_prediction()
    pred_info["E_hydration(kcal/mol)"].append(pred["E_hydration"])
    pred_info["LogP"].append(pred["LogP"])

pred_df: pd.DataFrame = pd.DataFrame(pred_info).set_index("file_handle")
out_dir = "./data/predictions"
os.makedirs(out_dir, exist_ok=True)
pred_df.to_csv(osp.join(out_dir, "sphysnet-mt.csv"))

tok = time.time()
print("Total time running sPhysNet-MT: {:.1f}s".format(tok - tic))
# On a single CPU:
# Total time running sPhysNet-MT: 204.7s
