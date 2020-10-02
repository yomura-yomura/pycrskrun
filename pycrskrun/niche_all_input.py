import numpy as np
from .input_lines import input_fields
from . import lib_niche_array_for_crsk
from .all_input import all_input


# delete keywords
deleted_keywords = [
    "ATMOSPHERE",
    "MAGNET",
    "CWAVLG",
    "ECUTS",
    "LONGI",
    "OBSLEV",
    "PAROUT",

    "CWAVRANG",
    "CWAVLG",
    "CERSIZ",
    "CERFIL",
    "CERQEF",
                
#    "CSCAT",
    "COREPOS",
    "TELESCOPE",
    ]
    
deleted_input_fields = input_fields[
    np.isin(
        input_fields.keyword,
        deleted_keywords
        )
    ]

niche_input_fields = np.delete(
    input_fields,
    np.argwhere(
        np.isin(
            input_fields.keyword,
            deleted_keywords
            )
        )
    )


def append(recarray, records):
    list_recarray = recarray.tolist()

    try:
        records_col_length = np.shape(records)[np.ndim(list_recarray)-1]
    except IndexError:
        raise ValueError("dimension mismatch")

    if np.shape(list_recarray)[-1] != records_col_length:
        raise ValueError("the number of columns mismatch")

    list_recarray.extend(records)

    names = tuple(recarray.dtype.fields.keys())
    formats = [v[0] for v in recarray.dtype.fields.values()]

    for i in range(len(formats)):
        if formats[i].kind in ("S", "U"):
            import re
            matched = re.match("([<>])([US])(\d+)", str(formats[i]))
            endian, type, str_length = matched.groups()

            str_length = max(max([len(row[i]) for row in records]), int(str_length))
            formats[i] = np.dtype(f"{endian}{type}{str_length}")

    return np.rec.array(list_recarray, names=names, formats=formats)


# add new keywords
import math
from numpy import dtype

niche_input_fields = append(
    niche_input_fields,
    [
        ("NICHE_COREPOS", dtype("d, d"), 2, math.floor(999/len(lib_niche_array_for_crsk.telescope()))),
        
    ]
)

from data.detector import crsk_wl_options as cwo

default_all_input = '''
MAGNET  21.76  45.80                     magnetic field centr. TALE Site.
ECUTS   0.3  0.3  0.001  0.001         energy cuts for particles: hadrons, muons, electrons, photons (GeV)
LONGI   T  1.  T  F                   longit.distr. & step size & fit & out

{}

ATMOSPHERE  6  T                        U.S. standard atmosphere 1976, atmospheric refraction

CERSIZ  1
CERQEF  T   T   F                       enabled atmospheric absorption on 2019-10-29

PAROUT  F  F
CERFIL  0
'''.format("\n".join(cwo.get_option_lines()))


class niche_all_input(all_input):
    def __init__(self, filename=None, input_string=None, with_comments=True, coordinate="NICHE"):
        self.coordinate = coordinate
        if filename is None:
            if input_string is not None:
                input_string = default_all_input + "\n" + input_string
            else:
                input_string = default_all_input
            super().__init__(filename, input_string, with_comments)
            self.input_fields = niche_input_fields
        else:
            with open(filename, "r") as f:
                lines = f.readlines()
                default_commands = [line for line in default_all_input.splitlines() if line.strip() != ""]

                will_be_deleted = []
                for deleted in default_commands + deleted_keywords:
                    matched = np.argwhere(np.char.startswith(lines, deleted))
                    if 0 < matched.size:
                        will_be_deleted.extend(matched.flatten())

                lines = np.delete(lines, will_be_deleted)
                input_string = "\n".join([line.rstrip() for line in lines]).replace(default_all_input, "")

            filename = None
            input_string = default_all_input + "\n" + input_string

            super().__init__(filename, input_string, with_comments,
#                             input_fields=np.append(deleted_input_fields, niche_input_fields))
                             input_fields=np.rec.array(np.append(deleted_input_fields.astype(niche_input_fields.dtype), niche_input_fields)))# temporaly
            self.input_fields = niche_input_fields

    def append(self, keyword, args=[], comment=""):
        if self.coordinate == "NICHE":
            self._validate_keyword(keyword, args)
            if keyword == "PHIP":
#                import code
#                code.interact(local=locals())
                args = (args[0] - 90 if -270 <= args[0] else args[0] + 270,
                        args[1] - 90 if -270 <= args[1] else args[1] + 270)
            elif keyword == "CSCAT":
                args = (args[0], args[2], args[1])
        elif self.coordinate == "CORSIKA":
            if keyword == "NICHE_COREPOS":
                args = (-args[1], args[0], args[2])
        else:
            raise ValueError("invalid coordinate type: {}".format(self.coordinate))

        super().append(keyword, args, comment)

    def get_extracted(self):
        s = [line for line in super().__str__().splitlines()[:-1] if not line.startswith("NICHE_COREPOS")]

        if np.isin("NICHE_COREPOS", self.input_array["keyword"]):
            rows = self.input_array[self.input_array.keyword == "NICHE_COREPOS"]
            for i, row in rows.reset_index().iterrows():
                s.append("")
                telescope = lib_niche_array_for_crsk.telescope(x_core=row["args"][0], y_core=row["args"][1],
                                                               print_obslevel_command=(i == 0))
                s.extend(str(telescope).splitlines())
        else:
            s.append("")
            telescope = lib_niche_array_for_crsk.telescope()
            s.extend(str(telescope).splitlines())

        return all_input(input_string="\n".join(s))


        
#f = niche_all_input()
