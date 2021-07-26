import hmac
import hashlib



G = (
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
)
P = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


def getHmac(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()


def hmacDrbg(entropy, string):
    material = entropy + string
    K = b"\x00" * 32
    V = b"\x01" * 32

    K = getHmac(K, V + b"\x00" + material)
    V = getHmac(K, V)
    K = getHmac(K, V + b"\x01" + material)
    V = getHmac(K, V)

    temp = b""
    while len(temp) < 32:
        V = getHmac(K, V)
        temp += V

    return temp[:32]

def pointAdd(point1, point2):
    # Returns the result of point1 + point2 according to the group law.
    if point1 is None:
        return point2
    if point2 is None:
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        return None

    if x1 == x2:
        m = (3 * x1 * x1) * pow(2 * y1, -1, P)
    else:
        m = (y1 - y2) * pow(x1 - x2, -1, P)

    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % P, -y3 % P)

    return result


def scalar_mult(k, point):
    # Returns k * point computed using the double and point_add algorithm.
    result = None
    addend = point

    while k:
        if k & 1:
            # Add.
            result = pointAdd(result, addend)
        # Double.
        addend = pointAdd(addend, addend)
        k >>= 1

    return result


def toDER(r, s): # Signature to DER format
    r = bytes.fromhex(r)
    s = bytes.fromhex(s)
    if r[0] > 0x80:
        r = bytes.fromhex("00") + r
    if s[0] > 0x80:
        s = bytes.fromhex("00") + s
    res = bytes.fromhex("02"+hex(len(r))[2:]) + r + bytes.fromhex("02"+hex(len(s))[2:]) + s
    res = bytes.fromhex("30"+hex(len(res))[2:]) + res

    return res.hex()


def signTransaction(seedHex, txHex):
    s256 = hashlib.sha256(hashlib.sha256(bytes.fromhex(txHex)).digest()).digest()
    drbg = hmacDrbg(entropy=bytes.fromhex(seedHex), string=s256)
    k = int.from_bytes(drbg, 'big')
    kp = scalar_mult(k, G)
    kpX = kp[0]
    r = kpX % N
    s = pow(k, -1, N) * (r * int(seedHex, 16)+int(s256.hex(), 16))
    s = s % N
    signature = toDER(hex(r)[2:].zfill(64), hex(s)[2:].zfill(64))
    signed_transaction = txHex[:-2] + hex(len(bytearray.fromhex(signature)))[2:] + signature

    return signed_transaction