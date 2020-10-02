
class logfile:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, "r") as f:
            self.lines = f.readlines()

    def get_all_input_lines(self):
        START_DATACARD_INPUT = " DATA CARDS FOR RUN STEERING ARE EXPECTED FROM STANDARD INPUT"
        END_DATACARD_INPUT = " END OF DATACARD INPUT"

        all_input_lines = None
        for line in self.lines:
            line = line.rstrip()
            if line == START_DATACARD_INPUT:
                all_input_lines = []
            if all_input_lines is not None:
                all_input_lines.append(line)
            if line == END_DATACARD_INPUT:
                break

        self.logfile.seek(0)

        return all_input_lines
        
    def get_time(self):
        TIME_INPUT = " PRESENT TIME :"

        import dateutil.parser
        times = [dateutil.parser.parse(line[len(TIME_INPUT):])
                 for line in self.lines if line.startswith(TIME_INPUT)]
                
        return times[-1] - times[0]


    def __str__(self):
        return "pycrskrun.logfile(filename='{}')".format(self.filename)

    def __repr__(self):
        return str(self)

