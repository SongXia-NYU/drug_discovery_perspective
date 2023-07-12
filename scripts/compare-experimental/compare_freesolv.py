import pandas as pd
import rdkit
from rdkit.Chem import MolFromSmiles, MolToInchiKey
import seaborn as sns
import matplotlib.pyplot as plt

freesolv_csv = "data/experimental_properties/freesolv.csv"
freesolv_df: pd.DataFrame = pd.read_csv(freesolv_csv, sep=";")

def smiles2inchi_key(smiles: str) -> str:
    mol = MolFromSmiles(smiles)
    inchi_key = MolToInchiKey(mol)
    return inchi_key

freesolv_df["InChIKey"] = freesolv_df["SMILES"].map(smiles2inchi_key)
freesolv_df = freesolv_df.set_index("InChIKey")

lig_info_csv = "data/FDA_kinase_ligand_binding_affinity/lig_info.csv"
lig_info_df: pd.DataFrame = pd.read_csv(lig_info_csv).set_index("InChIKey")

compare_df = freesolv_df.join(lig_info_df, how="inner", lsuffix="exp_")
print(compare_df)

sns.histplot(freesolv_df, x="experimental value (kcal/mol)")
plt.tight_layout()
plt.savefig("data/experimental_properties/freesolv.png")
