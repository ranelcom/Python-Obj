#!/usr/bin/python3

from subprocess import Popen
import sys

filename = sys.argv[1]
while True:
    print("\nIniciando " + filename)
    p = Popen("python3 " + filename, shell=True)
    p.wait()
