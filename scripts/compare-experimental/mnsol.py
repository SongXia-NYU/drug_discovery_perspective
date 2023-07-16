import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def formula2n_heavy(formula: str) -> int:
    ele: str = ""
    count: str = ""
    num_strs: list = [str(i) for i in range(10)]
    counter: dict = {}
    for c in formula:
        if c in num_strs:
            count += c
            continue
        if count:
            counter[ele] = int(count)
            ele, count = "", ""
        ele += c
    counter[ele] = int(count)
    
    nheavy = 0
    for ele in counter:
        if ele == "H":
            continue
        nheavy += counter[ele]
    return nheavy

def hist_num_heavy():
    mnsol_df = pd.read_excel("/scratch/sx801/scripts/drug_descovery_perspective/data/experimental_properties/MNSol_alldata.xls")
    mnsol_df["#HeavyAtoms"] = mnsol_df["Formula"].map(formula2n_heavy)
    sns.histplot(mnsol_df, x="#HeavyAtoms")
    plt.tight_layout()
    plt.savefig("data/experimental_properties/mnsol.nheavy.png")

    print(mnsol_df["#HeavyAtoms"].min())
    print(mnsol_df["#HeavyAtoms"].max())
    print(mnsol_df[mnsol_df["#HeavyAtoms"]==0])

if __name__ == "__main__":
    hist_num_heavy()
