# -*- coding: utf-8 -*-
import sys
from collections.abc import Iterable
support_unicode = sys.stdout.encoding.lower() == "utf-8"

# gamma, lepton, hadron and meson
particle_id_table = {
    1 : "γ"   if support_unicode else "gamma",
    2 : "e⁺"  if support_unicode else "positron",
    3 : "e⁻"  if support_unicode else "electron",
    5 : "μ⁺"  if support_unicode else "anti-muon",
    6 : "μ⁻"  if support_unicode else "muon",
    7 : "π⁰"  if support_unicode else "pi0",
    8 : "π⁺"  if support_unicode else "pi+",
    9 : "π⁻"  if support_unicode else "pi-",
    10: "K⁰L" if support_unicode else "K0L",
    11: "K⁺" if support_unicode else "K+",
    12: "K⁻" if support_unicode else "K-",
    13: "n",
    14: "p",
    15: u"p\u0304" if support_unicode else "anti-proton",
    16: "K⁰S" if support_unicode else "K0S",
    17: "η"   if support_unicode else "eta",
    # and so on...
}

chemical_symbols = (
None, 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og')

mass_numbers_in_stable = (
None, 1, 4, 7, 9, 11, 12, 14, 16, 19, 20, 23, 24, 27, 28, 31, 32, 35, 40, 39, 40, 45, 48, 51, 52, 55, 56, 59, 59, 64,
65, 70, 73, 75, 79, 80, 84, 85, 88, 89, 91, 93, 96, 98, 101, 103, 106, 108, 112, 115, 119, 122, 128, 127, 131, 133, 137,
139, 140, 141, 144, 145, 150, 152, 157, 159, 162, 165, 167, 169, 173, 175, 178, 181, 184, 186, 190, 192, 195, 197, 201,
204, 207, 209, 209, 210, 222, 223, 226, 227, 232, 231, 238, 237, 244, 243, 247, 247, 251, 252, 257, 258, 259, 262, 267,
268, 271, 270, 269, 278, 281, 281, 285, 286, 289, 289, 293, 293, 294)

# atom
particle_id_table.update({
    A * 100 + Z: (
        chemical_symbols[Z] if mass_numbers_in_stable[Z] == A
        else "{} (isotope A={})".format(chemical_symbols[Z], A)
    )
    for A in range(2, 56+1)
    for Z in range(1, 26+1)
})


particle_type_table = {v: k for k, v in particle_id_table.items()}
assert len(particle_type_table) == len(particle_id_table)


def id_to_type(id_):
    if isinstance(id_, Iterable):
        return map(id_to_type, id_)
    return particle_id_table[id_]


def type_to_id(type_):
    if isinstance(type_, str):
        pass
    elif isinstance(type_, bytes):
        return type_to_id(type_.decode())
    elif isinstance(type_, Iterable):
        return map(type_to_id, type_)
    return particle_type_table[type_]
