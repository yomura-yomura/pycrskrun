import numpy as np
import warnings
import pandas as pd
from . import input_lines


class all_input:
    def __init__(self, filename=None, input_string=None, with_comments=True, input_fields=None):
        self.filename = filename
        self.with_comments = with_comments

        if input_fields is None:
            input_fields = input_lines.input_fields
        self.input_fields = input_fields

        self.comment_lines = {}
        self.comment_after_commands = {}
        self.input_array = pd.DataFrame(columns=("keyword", "args", "i"))

        self.n_line = 0

        if filename is not None:
            with open(filename, "r") as f:
                self.append_lines(f.readlines())
        elif input_string is not None:
            self.append_lines(input_string.splitlines())

        for keyword in np.unique(self.input_array["keyword"]):
            args_list = self.input_array[self.input_array["keyword"] == keyword]
            if self.input_fields[self.input_fields.keyword == keyword][0].limit < len(args_list):
               warnings.warn(
                   "{} duplicate keywords '{}' defined ({} keyword(s) at most) ".format(
                       len(args_list), keyword, self.input_fields[self.input_fields.keyword == keyword][0].limit
                       ),
                   RuntimeWarning)

    def append_lines(self, input_lines):
        for line in input_lines:
            line = line.rstrip()
            try:
                self.append_line(line)
            except EOFError:
                self.n_line -= 1
                break

    def _validate_keyword(self, keyword, args):
        keyword = keyword.upper()
        if keyword == "EXIT":
            raise EOFError()
        if keyword not in self.input_fields.keyword:
            raise ValueError("Unknown keyword '{}'".format(keyword))

        field = self.input_fields[self.input_fields.keyword == keyword][0]
        if len(args) != field.arglength:
            raise ValueError("the number of argument(s) mismatched: {} ({} expected; {})".format(
                    len(args), 
                    field.arglength,
                    "type = {}".format(field.type.name) if len(field.type) == 0 else 
                    "types = {}".format([field.type[i].name for i in range(len(field.type))])
                    ))
        return field

    def append(self, keyword, args=[], comment=""):
        field = self._validate_keyword(keyword, args)

        self.input_array.loc[self.input_array.shape[0]] = [
            keyword,
            np.array([tuple(args)], dtype=field.type)[0],
            self.n_line
        ]

        if comment != "":
            self.comment_after_commands[self.n_line] = comment

        self.n_line += 1

    def append_line(self, line):
        returned = self.parse_input_line(line)
        if returned is not None:
            self.append(*returned)

    def keyword_hints(self):
        print(
            ", ".join(self.input_fields.keyword)
            )
            
    def parse_input_line(self, line):
        if (line             == "" or
            line[0]          == "*" or
            line[:1].upper() == "C " or
            line[:5].upper() == "IACT " or
            line[:6]         == "      "):
            self.comment_lines[self.n_line] = line
            self.n_line += 1
            return

        import re
        matched = re.match("(\S+)\s*(.*)", line)
        if matched is None:
            raise ValueError("Unrecognized format in line: '{}'".format(line))
        keyword, others = matched.groups()
        keyword = keyword.upper()

        if keyword not in self.input_fields.keyword:
            raise ValueError("Unknown keyword '{}'".format(keyword))

        field = self.input_fields[self.input_fields.keyword == keyword][0]

        matched = re.match("{}\s*(\S*.*)".format("\s+".join(["(\S+)" for _ in range(field.arglength)])), others)
        if matched is None:
            raise ValueError("{} argument(s) expected for a keyword '{}'".format(field.arglength, keyword))
        *args, comment = matched.groups()

        return (keyword,
                args,
                comment)

    def __str__(self):
        max_kw_len = max([len(kw) for kw in self.input_array["keyword"]])
        command_dict = {
            i: "{:<{max_kw_len}}  {}".format(
                self.input_array[self.input_array["i"] == i]["keyword"].iloc[0],
                "  ".join([
                        str(arg)
                        for arg in self.input_array[self.input_array["i"] == i]["args"].iloc[0]
                        ]),
                max_kw_len=max_kw_len
                )
            for i in range(self.n_line) if np.isin(i, self.input_array["i"])
            }

        if self.with_comments:
            max_cmd_len = max([len(cmd) for cmd in command_dict.values()])        
            commands = [
                "{:<{max_cmd_len}}  {}".format(
                    command_dict[i],
                    self.comment_after_commands[i] if i in self.comment_after_commands else "",
                    max_cmd_len=max_cmd_len
                    )
                if np.isin(i, self.input_array["i"])
                else self.comment_lines[i]
                for i in range(self.n_line)
                ]
        else:
            commands = command_dict.values()

        return ("\n".join(commands)
                + "\nEXIT")

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(str(self))

    def __repr__(self):
        return "{}(filename='{}'):\n{}".format(self.__class__.__name__, self.filename, self.__str__())

