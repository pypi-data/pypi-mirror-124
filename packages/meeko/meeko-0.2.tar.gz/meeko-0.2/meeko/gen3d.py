#!/usr/bin/env python

from rdkit import Chem
import sys


def fragment(rdkitmol):
    """ cut single bonds """
    return



rdkitmol = Chem.MolFromMolFile(sys.argv[1])

amide = Chem.MolFromSmarts('[NX3][CX3]=O')
amidine = Chem.MolFromSmarts('[NX3][CX3]=N')
amides = rdkitmol.GetSubstructMatches(amide)
amidines = rdkitmol.GetSubstructMatches(amidine)

print('amides', amides)
print('amidines', amidines)

no_break = set()
for (i, j, k) in amides + amidines:
    no_break.add((i, j))

print('no_break:', no_break)

for bond in rdkitmol.GetBonds():
    atom_bgn = bond.GetBeginAtom()
    atom_end = bond.GetEndAtom()
    i = atom_bgn.GetIdx()
    j = atom_end.GetIdx()
    do_not_break = False
    if (i, j) in no_break or (j, i) in no_break:
        do_not_break = True
    print('%8s %3d %3d %.1f %s %s'  % (bond.GetBondType(), i+1, j+1, bond.GetBondTypeAsDouble(), bond.GetIsConjugated(), do_not_break))
