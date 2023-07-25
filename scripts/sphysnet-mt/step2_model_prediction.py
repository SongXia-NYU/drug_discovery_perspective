"""
Make predictions using sPhysNet-MT
"""
from glob import glob
import os
import os.path as osp
import time
from argparse import ArgumentParser
from rdkit.Chem import SDMolSupplier, MolToInchiKey, MolFromSmiles
from typing import DefaultDict, Dict, List, Tuple, Union
import pandas as pd

from predict import EnsPredictor

# ----parsing arguments---- #
parser = ArgumentParser()
parser.add_argument("--smiles_list", nargs="+", required=True)
args = parser.parse_args()

# ----prepareing SMILES information for the FDA approved drugs---- #
# smiles_list contains SMILES information
smiles_list: List[str] = args.smiles_list
# file_handle_list contains file handles which is used as the file names
file_handle_list: List[str] = []
for smiles in smiles_list:
    inchi_key: str = MolToInchiKey(MolFromSmiles(smiles))
    file_handle_list.append(inchi_key)

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

for smiles, file_handle in zip(smiles_list, file_handle_list):
    mmff_sdf = osp.join("./data/mmff_geometries/conf_lowest", f"{file_handle}.sdf")
    pred_info["SMILES"].append(smiles)
    pred_info["InchiKey"].append(file_handle)

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

tok = time.time()
print("Total time running sPhysNet-MT: {:.1f}s".format(tok - tic))

pred_df: pd.DataFrame = pd.DataFrame(pred_info).set_index("InchiKey")
print("The prediction by sPhysNet-MT-ens5: ")
print(pred_df)

