from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import pandas as pd

def csd2props(csd_id: str):
    exp_props: dict = {"expLogP": None, "ALOGPS": None, "Chemaxon": None}
    rcsb_url = f"https://www.rcsb.org/ligand/{csd_id}"
    r = requests.get(rcsb_url)
    soup = BeautifulSoup(r.content, 'html5lib')
    db_id_entry = soup.find(attrs={"id": "drugBankID"})
    if db_id_entry is None:
        return {}
    db = db_id_entry.find(attrs={"rel": "noopener"})
    db_id: str = db.string

    db_url = f"https://go.drugbank.com/drugs/{db_id}"
    r = requests.get(db_url)
    soup = BeautifulSoup(r.content, 'html5lib')
    exp_table = soup.find("table", attrs={"id": "experimental-properties"})
    if exp_table:
        for row in exp_table.find_all("tr"):
            row_vals = [ele.string.strip() for ele in row.find_all("td")]
            if len(row_vals) == 0:
                continue
            if row_vals[0] == "logP":
                exp_props["expLogP"] = float(row_vals[1])
                break

    pred_table = soup.find("table", attrs={"id": "drug-moldb-properties"})
    for row in pred_table.find_all("tr"):
        row_vals = [ele.string.strip() if ele.string else None for ele in row.find_all("td")]
        if len(row_vals) == 0:
            continue
        if row_vals[0] == "logP":
            exp_props[row_vals[2]] = float(row_vals[1])

    return exp_props


def get_exp_props():
    pred_csv = "data/predictions/sphysnet-mt.csv"
    pred_df = pd.read_csv(pred_csv)

    exp_info = defaultdict(lambda: [])
    for file_handle in pred_df["file_handle"]:
        csd_id = file_handle.split("_")[-1]
        this_info: dict = csd2props(csd_id)
        for key in this_info:
            exp_info[key].append(this_info[key])
        if not this_info:
            continue
        exp_info["file_handle"].append(file_handle)
    exp_df = pd.DataFrame(exp_info).set_index("file_handle")
    pred_df = pred_df.set_index("file_handle")
    combined_df = pred_df.join(exp_df)
    combined_df.to_csv("data/predictions/sphysnet-mt_vs_exp.csv")

if __name__ == "__main__":
    get_exp_props()
