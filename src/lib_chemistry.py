#!/usr/bin/env python

# Draws a molecule from its InChi representation
# Dependencies: rdkit

import argparse

from rdkit import Chem
from rdkit.Chem import AllChem, Draw
from rdkit.Chem.inchi import MolFromInchi


def draw_inchi(inchi, imgfile):
    molecule = Chem.AddHs(MolFromInchi(inchi))
    AllChem.EmbedMolecule(molecule)
    AllChem.MMFFOptimizeMolecule(molecule)
    Draw.MolToFile(molecule, imgfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inchi')
    parser.add_argument('--imgfile')
    args = parser.parse_args()

    draw_inchi(args.inchi, args.imgfile)
