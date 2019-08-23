import argparse
import hashlib

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def encode_base58(s):
    # determine how many 0 bytes (b'\x00') s starts with
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    # convert to big endian integer
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result


def hash256(s):
    """2 iterations of sha256"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def wif(pk, compressed=False, testnet=False):
    """Wallet import format for private key. Private key is a 32 bit bytes"""
        prefix = b"\x80"
        suffix = b''
    extended_key = prefix + pk + suffix
    assert(len(extended_key) == 33 or len(extended_key) == 34)
    final_key = extended_key + hash256(extended_key)[:4]
    WIF = encode_base58(final_key)
    return WIF



# Example usage
# python3 wif.py -b 0010100010001111001110011011101111111101001101101101101001011010000100101101000101100010110010110001100010010111110010010000001000101000100010110011100110111011001101101101101001011010000100101101000101100010110010110001100010010111110010010000001000111101

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--binary", type=str, default=False, help="result of 256 coin flips eg 001001...")
    args = parser.parse_args()
    if args.binary:
        assert(len(args.binary) == 256)
        key = hex(int(args.binary, 2)).replace('0x', "")
        WIF = wif(bytes.fromhex(key), args.compressed, args.testnet)
        print("WIF = {}".format(WIF))

# Pulled from https://gist.github.com/fiddler-yee/13b7638893de687e16e839959d077988 with test code and unused options removed.
