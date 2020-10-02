#!/usr/bin/env python3
import sys
from pycrskrun import logfile

log = logfile(sys.argv[1])
print("* run time = {}".format(log.get_time()))
