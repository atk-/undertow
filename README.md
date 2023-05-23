# undertow

A naively simple WAV file steganography program.

# Usage

To hide data into a cover file and write the result into a stego file:

`python undertow.py -m "[message]" ([-s stride]) [cover-file] [stego-file]`

To reveal data in a stego file:

`python undertow.py ([-s stride]) [stego-file]`

# Features

The stride parameter controls how far apart consecutive characters in the message are written in the file. Several messages can be written into a single file using different stride values. Using prime numbers as stride values ensures two messages with different strides will never overlap and clobber each other.

# Keywords

steganography, stego, information hiding, uncover
