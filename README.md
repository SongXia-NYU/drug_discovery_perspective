# Integrated Molecular Modeling and Machine Learning for Drug Design
In this tutorial, we will demonstrate how to use calculation and analysis tools mentioned in the perspective paper [Integrated Molecular Modeling and Machine Learning for Drug Design]().
![](./data/example_1m17.png)

## A. Protein Pocket Identification and Analysis with AlphaSpace

## B. Protein-ligand Binding Affinity Prediction with $\Delta_{LinF9}XGB$

## C. Small Molecule Properties Prediction with sPhysNet-MT-ens5
### Environment Setup
`conda create -n sphysnet-mt python==3.8 -y`

`conda activate sphysnet-mt`

`bash sPhysNet-MT/bash_scripts/install_env_linux.bash`

### Prediction with sPhysNet-MT-ens5
The SMILES of Erlotinib is `COCCOc1cc2c(cc1OCCOC)ncnc2Nc3cccc(c3)C#C`
