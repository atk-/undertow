# undertow

A naively simple WAV file steganography program.

# Usage

To hide data into a cover file and write the result into a stego file:

`python undertow.py -m "[message]" ([-s stride]) [cover-file] [stego-file]`

To reveal data in a stego file:

`python undertow.py ([-s stride]) [stego-file]`

# Keywords

steganography, stego, information hiding, uncover
