import pandas as pd
import rdkit
from rdkit.Chem import MolFromSmiles, MolToInchiKey
import seaborn as sns
import matplotlib.pyplot as plt

exp_log_p_csv = "data/experimental_properties/logP_labels.csv"
exp_log_p_df: pd.DataFrame = pd.read_csv(exp_log_p_csv)

def smiles2inchi_key(smiles: str) -> str:
    mol = MolFromSmiles(smiles)
    inchi_key = MolToInchiKey(mol)
    return inchi_key

def hist_props():
    exp_log_p_df["InChIKey"] = exp_log_p_df["SMILES"].map(smiles2inchi_key)
    exp_log_p_df = exp_log_p_df.set_index("InChIKey")

    lig_info_csv = "data/FDA_kinase_ligand_binding_affinity/lig_info.csv"
    lig_info_df: pd.DataFrame = pd.read_csv(lig_info_csv).set_index("InChIKey")

    compare_df = exp_log_p_df.join(lig_info_df, how="inner", lsuffix="exp_")
    print(compare_df)

    sns.histplot(exp_log_p_df, x="logP")
    plt.tight_layout()
    plt.savefig("data/experimental_properties/logP_labels.png")


def smiles2n_heavy(smiles: str) -> int:
    mol = MolFromSmiles(smiles)
    return mol.GetNumHeavyAtoms()

def hist_num_heavy():
    exp_log_p_df["#HeavyAtoms"] = exp_log_p_df["SMILES"].map(smiles2n_heavy)
    sns.histplot(exp_log_p_df, x="#HeavyAtoms")
    plt.tight_layout()
    plt.savefig("data/experimental_properties/logP.nheavy.png")

    print(exp_log_p_df["#HeavyAtoms"].min())
    print(exp_log_p_df["#HeavyAtoms"].max())

if __name__ == "__main__":
    hist_num_heavy()
