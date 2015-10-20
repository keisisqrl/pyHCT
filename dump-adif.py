#!/usr/bin/env python

import argparse
import serial
import re

parser = argparse.ArgumentParser(
  description='Load ADIF from a QRPworks HCT or SideKar module.',
  epilog="use 'python -m serial.tools.list_ports' to find port")
parser.add_argument('port',help='serial port to be used')
parser.add_argument('output',
  help='.adi file to be written (WILL BE OVERWRITTEN)')
args = parser.parse_args()

ser = serial.Serial(args.port,timeout=2)

outfile = open(args.output,'w')

adif_rem = -1

print 'Waiting for ADIF...'

while True:
  hct_in = ser.read(512)
  print hct_in
  if '{' in hct_in and adif_rem == -1:
    adif_rem = int(re.split('[{}]',hct_in)[1])
  elif adif_rem > 0:
    if '[' in hct_in:
      hct_in = hct_in.split('[')[1]
    if len(hct_in) >= adif_rem:
      outfile.write(hct_in[:adif_rem])
      break
    else:
      outfile.write(hct_in)
      adif_rem = adif_rem - len(hct_in)
  if not adif_rem:
    break
