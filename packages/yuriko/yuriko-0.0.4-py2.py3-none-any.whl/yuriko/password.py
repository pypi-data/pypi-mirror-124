import hashlib
import random
import time


def gen_password(
        length=12,
        allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Return a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    random.seed(
        hashlib.sha256(
            ('y%s%s' % (random.getstate(), time.time())).encode()
        ).digest()
    )
    return ''.join(random.choice(allowed_chars) for i in range(length))
