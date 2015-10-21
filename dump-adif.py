#!/usr/bin/env python

import argparse
import serial
import re

# This should hopefully be self-explanatory
parser = argparse.ArgumentParser(
  description='Load ADIF from a QRPworks HCT or SideKar module.',
  epilog="use 'python -m serial.tools.list_ports' to find port")
parser.add_argument('port',help='serial port to be used')
parser.add_argument('output',
  help='.adi file to be written (WILL BE OVERWRITTEN)')
args = parser.parse_args()

# Open serial port. Errors passed to user. Timeout may be tuned.
ser = serial.Serial(args.port,timeout=.1)

# Open output file. Errors, again, passed to user.
outfile = open(args.output,'w')

# Prep this variable. We assume we don't start in ADIF.
in_adif = False

print 'Waiting for ADIF...'


# This is an unbounded, but not infinite, loop.
# The code within should exit.
while True: 
  hct_in = ser.read(512) # Read up to 512 bytes.
  # If we're not in ADIF, find the start
  if not in_adif: # Data not started yet
    if '[' in hct_in: # if ADIF starts here:
      in_adif = True # set in_adif for future loops
      hct_in = hct_in.split('[',1)[1] # strip any preceeding data
    else: # otherwise,
      continue # jump to the next loop - more data!
  # The continue line above should guarantee this
  assert in_adif, "BUG: in_adif not set, but ADIF input reached"
  # Look for the end of the ADIF data
  if '\n]' in hct_in: # If the end of ADIF happens in collected data:
    in_adif = False # Done after this loop
    hct_in = hct_in.rsplit(']',1)[0] # Strip late data
  # The next statement deals with an edge case:
  # what happens if '\n]' happens across reads?
  if hct_in.endswith('\n'): # If the read buffer ends with newline
    next_byte = ser.read(1) # Read one more byte...
    if next_byte == ']': # if it's a close brace
      in_adif = False # we're done with ADIF; throw it away
    else: # otherwise
      hct_in = hct_in + next_byte # append the next byte to hct_in
  # We have our current ADIF data. Dump it.
  outfile.write(hct_in) # write the current data to the file
  # Check if we should loop again
  if not in_adif: # If we're done with ADIF
    break # Exit the while loop, terminate the script.
