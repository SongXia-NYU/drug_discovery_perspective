"""
Generate MMFF-optimized geometries from SMILES using the protocol described in the Figure 2 of https://pubs.acs.org/doi/10.1021/acs.jctc.2c01024?ref=pdf

1. Up to 300 conformations are generated with ETKDG in RDKit and optimized with MMFF94. 
2. The one conformation with the lowest MMFF level energy is selected for each compound. 
"""
from typing import List
import pandas as pd
import os
import time
from Frag20_prepare.DataGen.genconfs import runGenerator

lig_info_df: pd.DataFrame = pd.read_csv("data/FDA_kinase_ligand_binding_affinity/lig_info.csv")

# ----prepareing SMILES information for the FDA approved drugs---- #
# smiles_list contains SMILES information
smiles_list: List[str] = []
# file_handle_list contains file handles which is used as the file names
file_handle_list: List[str] = []
for i in range(lig_info_df.shape[0]):
    this_info: pd.Series = lig_info_df.iloc[i]
    smiles: str = this_info["SMILES"]
    pdb_id: str = this_info["PDB"]
    lig_id: str = this_info["LIG"]
    file_handle: str = f"{pdb_id}_{lig_id}"

    smiles_list.append(smiles)
    file_handle_list.append(file_handle)

# ----generate up to 300 conformations and optimize with MMFF---- #
tic = time.time()
save_folder = "./data/mmff_geometries/confs_300"
os.makedirs(save_folder, exist_ok=True)
runGenerator(file_handle_list, smiles_list, "fda_drugs", save_folder)
tok = time.time()
print("Total time running conformation generation and MMFF optimization: {:.1f}s".format(tok - tic))

# TODO: Select the conformation with the lowest MMFF-optmized energy
save_folder = "./data/mmff_geometries/conf_lowest"
