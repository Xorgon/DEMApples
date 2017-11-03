import struct


def float_to_bin(num):
    """ Converts a float to a single precision float binary representation. """
    return bin(struct.unpack('!I', struct.pack('!f', num))[0])[2:].zfill(32)


def bin_to_float(binary):
    """ Converts a single precision float binary representation to a float. """
    return struct.unpack('!f', struct.pack('!I', int(binary, 2)))[0]
