# Integrated Molecular Modeling and Machine Learning for Drug Design
In this tutorial, we will demonstrate how to use calculation and analysis tools mentioned in the perspective paper [Integrated Molecular Modeling and Machine Learning for Drug Design]().

## Clone this Repo
```
git clone --recurse-submodules -j8 https://github.com/SongXia-NYU/drug_discovery_perspective.git
```

![](./data/example_1m17.png)

## A. Protein Pocket Identification and Analysis with AlphaSpace 2.0
### [AlphaSpace 2.0](https://github.com/RedesignScience/AlphaSpace2) Environment Setup; [tutorials](https://github.com/Vanabins28/AlphaSpace2_Tutorials)
```bash
conda create -n alphaspace2 python==3.8 -y
conda activate alphaspace2
git clone https://github.com/lenhsherr/AlphaSpace2.git
cd AlphaSpace2
pip install .
```

If you have trouble installing mdtraj, try installing it with conda
``` bash
conda install -c conda-forge mdtraj
```

Proper preparation of the receptors for the calculation of β-score requires the installation of 3rd party tools
- [`pdb2pqr30`](https://pdb2pqr.readthedocs.io/en/latest/) 
- [`MGLtools`](https://ccsb.scripps.edu/mgltools/)

To run this conda in the jupyter notebook ([if not installed yet](https://jupyter.org/install)), keep the conda environment active and run:
```bash
pip install ipykernel
python -m ipykernel install --user --name alphapsace2 --display-name AS2
```
Now this environment will be available to run with jupyter notebooks.

### Proper preparation of receptors to calculate the β-score of the 1M17 structure
As the β-score is analagous to the Vina score, we follow a similar protocol of Vina preparations except we exclude hydrogens.
1) First remove the crystal waters, split the ligand and receptor into separate files. Model the missing residues as needed.
2) Use [`pdb2pqr30`](https://pdb2pqr.readthedocs.io/en/latest/) to add missing heavy atoms to individual residues, protonate to generate a `.pqr` file for the receptor. 
2) Then you can delete the last two columns of the `.pqr` file so that it can be input into the `prepare_receptor4.py` tool. Input the `.pqr` file use to [`prepare_receptor4.py` function from MGLtools](https://ccsb.scripps.edu/mgltools/) to generate the charges and output a `.pdbqt` file

### Calculation of AlphaSpace2.0 features
You can now run the corresponding jupyter notebook in `script/1M17_AS2.ipynb`. There you can run and determine the features of the Erlotinib binding pockets of EGFR
```bash
jupyter notebook jupyter_notebooks/1M17_AS2.ipynb
```

## B. Binding affinity prediction of crystal EGFR-Erlotinib pose with $\Delta_\text{{Lin\_F9}}\text{XGB}$
### Environment Setup
You can follow [this link to install $\Delta_\text{{Lin\_F9}}\text{XGB}$](https://github.com/cyangNYU/delta_LinF9_XGB). A linux system is required to run Smina, the docking tool that is used to incorporate the Lin_F9 scoring function.

Similar to AlphaSpace2, it is necessary to install 3rd packages to properly prepare the receptors
- [`pdb2pqr30`](https://pdb2pqr.readthedocs.io/en/latest/) 
- [`MGLtools`](https://ccsb.scripps.edu/mgltools/)

### Preparation of input files
1) Split the ligand and receptor into separate files. Retain the crystal waters in the receptor file. Model the missing residues as needed
2) Use [`pdb2pqr30`](https://pdb2pqr.readthedocs.io/en/latest/) to add missing heavy atoms to individual residues and protonate them. This generates a `.pqr` file for the receptor. 
3) Then you can delete the last two columns of the `.pqr` file so that it can be input into the `prepare_receptor4.py` tool. Input the altered `.pqr` file to [`prepare_receptor4.py` function from MGLtools](https://ccsb.scripps.edu/mgltools/) to generate the charges and output a `.pdbqt` file. Use the `-U nphs` flag to retain only the non-polar hydrogens.
4) Use the `prepare_ligand4.py` tool to generate charges for the ligand and output a `.pdbqt` file. Use the `-U nphs` flag to retain only the non-polar hydrogens.

### Calculation of $\Delta_\text{{Lin\_F9}}\text{XGB}$
Once you've done these preparation, generate the features used by the XGBoost model with `delta_LinF9_XGB/script/runFeatures.sh`. It is important to input the altered `.pqr` file and `.pdbqt` files into `runFeatures.sh` script

Then you can run the `delta_LinF9_XGB/script/runXGB.py` script. This script will run Smina with the Lin_F9 scoring function, calculate all of the appropriate features, and run the XGBoost model to predict the correction to the Lin_F9 scoring function.

## C. Small Molecule Properties Prediction with sPhysNet-MT-ens5
### Environment Setup
```bash
conda create -n sphysnet-mt python==3.8 -y
conda activate sphysnet-mt
bash sPhysNet-MT/bash_scripts/install_env_linux.bash
```

### Prediction with sPhysNet-MT-ens5
The SMILES of Erlotinib is `COCCOc1cc2c(cc1OCCOC)ncnc2Nc3cccc(c3)C#C`. To run prediction:

```bash
bash run_sphysnet_mt.sh "COCCOc1cc2c(cc1OCCOC)ncnc2Nc3cccc(c3)C#C"
```

You can run multiple compounds at once. For example: 
```bash
bash run_sphysnet_mt.sh "COCCOc1cc2c(cc1OCCOC)ncnc2Nc3cccc(c3)C#C C[C@H](c1c(ccc(c1Cl)F)Cl)Oc2cc(cnc2N)c3cnn(c3)C4CCNCC4 C[C@@H]1CCN(C[C@@H]1N(C)c2c3cc[nH]c3ncn2)C(=O)CC#N"
```
