#!/usr/bin/env python3

import sys
import smedia

def usage():
  print('{} SMEDIA_HEADER SMAZ_UNPACKED_LENGTH SMAZ_CHUNKS... OUT'.format(sys.argv[0]))

if len(sys.argv) < 4:
  usage()
  sys.exit(1)

smedia.pack(sys.argv[1], int(sys.argv[2]), sys.argv[3:-1], sys.argv[-1])
