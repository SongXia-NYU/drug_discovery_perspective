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
from rdkit.Chem import SDMolSupplier, MolToInchiKey, MolFromSmiles
from glob import glob
import subprocess
from argparse import ArgumentParser
from Frag20_prepare.DataGen.genconfs import runGenerator

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

# ----generate up to 300 conformations and optimize with MMFF---- #
multi_conf_folder = "./data/mmff_geometries/confs_300"
os.makedirs(multi_conf_folder, exist_ok=True)
print("Start conformation generation. For each compound, up to 300 conformations will be generated and optimized.")
print(f"Total number of molecules: {len(smiles_list)}")
tic = time.time()
runGenerator(file_handle_list, smiles_list, "fda_drugs", multi_conf_folder)
tok = time.time()
print("Total time running conformation generation and MMFF optimization: {:.1f}s".format(tok - tic))

# ----Select the conformation with the lowest MMFF-optmized energy---- #
tic = time.time()
lowest_conf_folder = "./data/mmff_geometries/conf_lowest"
os.makedirs(lowest_conf_folder, exist_ok=True)
print("Start selecting the conformation with the lowest MMFF energy.")
for file_handle in file_handle_list:
    multi_conf_sdf: str = osp.join(multi_conf_folder, f"{file_handle}_confors.sdf")
    with SDMolSupplier(multi_conf_sdf, removeHs=False) as suppl:
        mol_list = [mol for mol in suppl]
    lowest_energy_mol: rdkit.Chem.rdchem.Mol = None
    lowest_energy: float = np.inf

    for mol in mol_list:
        mmff_energy: float = float(mol.GetProp("energy_abs"))
        if mmff_energy < lowest_energy:
            lowest_energy = mmff_energy
            lowest_energy_mol = mol
    writer = rdkit.Chem.SDWriter(osp.join(lowest_conf_folder, f"{file_handle}.sdf"))
    writer.write(lowest_energy_mol)
tok = time.time()
print("Total time running conformation selection: {:.1f}s".format(tok - tic))
