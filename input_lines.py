import numpy as np
from numpy import dtype

A = np.unicode
F = np.float64
I = np.int32  # maybe
L = np.bool

from collections import namedtuple

input_fields = np.rec.array([
    ["RUNNR", dtype("i"), 1, 1],
    ["EVTNR", dtype("i"), 1, 1],
    ["SEED", dtype("i, i, i"), 3, 14],
    ["NSHOW", dtype("i"), 1, 1],
    ["PRMPAR", dtype("i"), 1, 1],
    ["ERANGE", dtype("d, d"), 2, 1],
    ["ESLOPE", dtype("d"), 1, 1],
    ["THETAP", dtype("d, d"), 2, 1],
    ["PHIP", dtype("d, d"), 2, 1],
    #        ["VIEWCONE"  , , ],
    ["FIXCHI", dtype("d"), 1, 1],
    ["TSTART", dtype("d"), 1, 1],
    ["FIXHEI", dtype("d, i"), 2, 1],
    ["IMPACT", dtype("d, d"), 2, 1],
    #        ["INFILE" , dtype("U")       , 1],
    #        ["OUTFILE" , dtype("")    , ],
    ["ATMOD", dtype("i"), 1, 1],
    #        ["ATMA"   , dtype("")    , ],
    ["ATMOSPHERE", dtype("i, U1"), 2, 1],
    ["MAGNET", dtype("d, d"), 2, 1],
    ["HILOW", dtype("d"), 1, 1],
    ["STEPFC", dtype("d"), 1, 1],
    ["THIN", dtype("d, d, d"), 3, 1],
    ["THINH", dtype("d, d"), 2, 1],
    ["THINEM", dtype("d, d"), 2, 1],
    ["CORECUT", dtype("d"), 1, 1],
    ["ECUTS", dtype("d, d, d, d"), 4, 1],
    ["LONGI", dtype("U1, d, U1, U1"), 4, 1],
    ["OBSLEV", dtype("d"), 1, 10],
    ["MAXPRT", dtype("i"), 1, 1],
    ["ECTMAP", dtype("d"), 1, 1],
    ["DIRECT", dtype("U239"), 1, 1],
    ["PAROUT", dtype("U1, U1"), 2, 1],
    ["CWAVLG", dtype("d, d"), 2, 1],
    ["CERSIZ", dtype("d"), 1, 1],
    ["CERFIL", dtype("i"), 1, 1],
    ["CERQEF", dtype("U1, U1, U1"), 3, 1],
    ["CWAVRANG", dtype("d, d"), 2, 1],
    ["CSCAT", dtype("i, d, d"), 3, 1],
    ["COREPOS", dtype("d, d"), 2, 20],
    ["TELESCOPE", dtype("d, d, d, d"), 4, 999],
    ["TELFIL", dtype("U512"), 1, 1],
    ["EXIT", None, 0, 1],

], names=("keyword", "type", "arglength", "limit"))
