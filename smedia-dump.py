#!/usr/bin/env python3

import sys
from struct import *

def find_sequence(d, sequence, off=0):
  for start in range(off, len(d) - len(sequence)):
    end = start + len(sequence)
    if d[start:end] == sequence:
      return start, end
  return None, None

d = open(sys.argv[1], 'rb').read()

off = 0
smedia_idx = 0
while 1:
  smedia_off, off = find_sequence(d, b'SMEDIA02', off)
  if smedia_off == None:
    break

  unk = unpack_from('>I', d, off)[0]
  off += 4
  header_length = unpack_from('>I', d, off)[0]
  off += 4
  data_length = unpack_from('>I', d, off)[0]
  off += 4
  print('0x{:06x} SMEDIA02: unk=0x{:x}, header_length={:d}, data_length={:d}'.format(
      smedia_off, unk, header_length, data_length))

  open('smedia-header-{}.bin'.format(smedia_idx), 'wb').write(d[smedia_off+off:smedia_off+header_length])

  smaz_off = smedia_off + header_length
  assert(d[smaz_off:smaz_off+4] == b'SMAZ')
  off = smaz_off + 4
  unpacked_chunk_length = unpack_from('>I', d, off)[0]
  off += 4
  print('  0x{:06x} SMAZ: unpacked_chunk_length={:d}'.format(smaz_off, unpacked_chunk_length))

  checksum, length = unpack_from('>2I', d, smaz_off - 8)
  print('                 unk=0x{:08x}, total_unpacked_length={:d}'.format(checksum, length))
  orig_data_length = data_length

  data_length -= 8
  smaz_idx = 0

  with open('smaz-{}.bin'.format(smedia_idx), 'wb') as smaz_file:
    while data_length > 8:
      chunk_off = off
      unpacked_length = unpack_from('>I', d, off)[0]
      off += 4
      packed_length = unpack_from('>I', d, off)[0]
      off += 4

      smaz = d[off:off+packed_length]
      #open('smaz-{}-{}.bin'.format(smedia_idx, smaz_idx), 'wb').write(smaz)
      smaz_file.write(smaz)

      off += packed_length
      print('    0x{:06x} unpacked_length={:d}, packed_length={:d}'.format(chunk_off, unpacked_length, packed_length))
      data_length -= packed_length + 8

      smaz_idx += 1

  # Validate the termination bytes
  print('    {}-padding bytes: {}'.format(data_length,
      ' '.join(['{:02x}'.format(b) for b in d[off:off+data_length]])))
  assert(d[off:off+data_length] == b'\x00' * data_length)
  assert(data_length < 8)

  off += data_length
  smedia_idx += 1

  print('')
