"""
undertow.py:

A naively simple method of hiding text information into a WAV file. Replaces every Nth sample with
value 256 * (X // 256) + C, where X is the original sample value and C is the character code of
the letter in question. The message ends with the null character (C = 0).

Using prime numbers as the values of stride N it is possible to hide multiple overlapping
messages without fear of them clobbering each other.
"""
import argparse
import audioop
import struct
import wave


def extract(fname, stride):
    """Extract a message from the given file using the given stride value."""
    inf = wave.open(fname)
    width = inf.getsampwidth()
    data = inf.readframes(-1)

    message = ''

    for n in range(stride, len(data) // width, stride):
        sample = audioop.getsample(data, width, n)
        char = sample % 256
        if char == 0:
            break
        message += chr(char)

    return message


def encode(fname, message, stride, outfile):
    """Encode a message into the WAV file fname with the given stride, then write it into
    outfile."""
    message += '\x00'
    inf = wave.open(fname)
    params = inf.getparams()
    width = inf.getsampwidth()

    data = inf.readframes(-1)

    ax = [audioop.getsample(data, width, n) for n in range(stride, len(data) // width, stride)]
    mx = [a // 256 * 256 + ord(c) for a, c in zip(ax, message)]

    out = wave.open(outfile, 'w')
    out.setparams(params)

    xdata = data[:width * stride]
    data = data[width * stride:]

    while mx:
        val = mx.pop(0)
        xdata += struct.pack('<h', val)
        xdata += data[width:width * stride]
        data = data[width * stride:]

    xdata += data
    out.writeframes(xdata)
    out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=str)
    parser.add_argument('--message', '-m', type=str, nargs='?', help="the message to hide")
    parser.add_argument('--output', '-o', type=str, nargs='?',
                        help="the file to write output into")
    parser.add_argument('--stride', '-s', type=int, nargs='?', default=2999,
                        help="the stride in samples between consecutive characters")

    args = parser.parse_args()

    if args.message is None:
        # extraction mode
        message = extract(args.inputfile, stride=args.stride)
        print('extracted message: %s' % message)
    else:
        assert args.message is not None and args.output is not None
        # encoding mode
        encode(args.inputfile, args.message, args.stride, args.output)
