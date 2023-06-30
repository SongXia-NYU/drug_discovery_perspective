"""
Generate MMFF-optimized geometries from SMILES using the protocol described in the Figure 2 of https://pubs.acs.org/doi/10.1021/acs.jctc.2c01024?ref=pdf

1. Up to 300 conformations are generated with ETKDG in RDKit and optimized with MMFF94. 
2. The one conformation with the lowest MMFF level energy is selected for each compound. 
"""
from typing import List
import pandas as pd
import os
import os.path as osp
import time
import rdkit
import numpy as np
import shutil
from rdkit.Chem import SDMolSupplier
from glob import glob
import subprocess
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
multi_conf_folder = "./data/mmff_geometries/confs_300"
os.makedirs(multi_conf_folder, exist_ok=True)
runGenerator(file_handle_list, smiles_list, "fda_drugs", multi_conf_folder)
tok = time.time()
print("Total time running conformation generation and MMFF optimization: {:.1f}s".format(tok - tic))
# On a single CPU:
# >>> Total time running conformation generation and MMFF optimization: 1650.3s

# ----Select the conformation with the lowest MMFF-optmized energy---- #
tic = time.time()
lowest_conf_folder = "./data/mmff_geometries/conf_lowest"
os.makedirs(lowest_conf_folder, exist_ok=True)
multi_conf_sdfs: List[str] = glob(osp.join(multi_conf_folder, "*_*_confors.sdf"))
for multi_conf_sdf in multi_conf_sdfs:
    with SDMolSupplier(multi_conf_sdf, removeHs=False) as suppl:
        mol_list = [mol for mol in suppl]
    lowest_energy_mol: rdkit.Chem.rdchem.Mol = None
    lowest_energy: float = np.inf

    for mol in mol_list:
        mmff_energy: float = float(mol.GetProp("energy_abs"))
        if mmff_energy < lowest_energy:
            lowest_energy = mmff_energy
            lowest_energy_mol = mol
    file_handle: str = osp.basename(multi_conf_sdf).split("_confors")[0]
    writer = rdkit.Chem.SDWriter(osp.join(lowest_conf_folder, f"{file_handle}.sdf"))
    writer.write(lowest_energy_mol)
tok = time.time()
print("Total time running conformation selection: {:.1f}s".format(tok - tic))
# On a single CPU:
# >>> Total time running conformation selection: 3.7s

# ----Clean up---- #
# archive the SDF files with multiple conformations as they are no longer needed
subprocess.run("tar caf confs_300.tar.gz confs_300/", shell=True, check=True, cwd="./data/mmff_geometries")
shutil.rmtree(multi_conf_folder)
