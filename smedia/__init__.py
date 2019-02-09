import struct as s

unpacked_chunk_length = 0x80000
padding = 4  # Any length above this value appears to be valid

def pack(smedia_header_path, smaz_unpacked_length, smaz_chunk_paths, out_path):
  smedia_header = open(smedia_header_path, 'rb').read()
  smaz_chunks = [open(f, 'rb').read() for f in smaz_chunk_paths]

  with open(out_path, 'wb') as out:
    out.write(b'SMEDIA02')
    out.write(b'\x00\x00\x00\x70')
    out.write(s.pack('>I', len(smedia_header) + 20))

    smaz_length = sum(len(chunk) + 4 * 2 for chunk in smaz_chunks) + 4 * 2

    out.write(s.pack('>I', smaz_length + padding))

    out.write(smedia_header)

    out.write(b'SMAZ')
    out.write(s.pack('>I', unpacked_chunk_length))

    for chunk in smaz_chunks:
      out.write(s.pack('>I', min(unpacked_chunk_length, smaz_unpacked_length)))
      smaz_unpacked_length -= unpacked_chunk_length

      out.write(s.pack('>I', len(chunk)))
      out.write(chunk)

    out.write(b'\x00' * padding)
