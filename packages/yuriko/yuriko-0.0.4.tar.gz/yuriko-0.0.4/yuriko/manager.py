import binascii
import hashlib
import string

from Crypto import Random
from Crypto.Cipher import AES


class NotesManager:

    KEYS_KEY = 'keys'
    TEST_KEY = 'test'
    TEST_VAL = 'ok'

    def __init__(self, path, password):
        assert path

        self.path = path
        self.password = password

        self.notes = {}
        self.validate_password(password=password)

        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    if ':' not in line:
                        continue
                    key = line.split(':')[0]
                    val = ':'.join(line.split(':')[1:]).strip()
                    self.notes[key] = val
        except IOError:
            pass

    def save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            for k in sorted(self.notes.keys()):
                v = self.notes[k]
                f.write('{}:{}\n'.format(k, v))

    @classmethod
    def encrypt(cls, val, key):
        key = key.encode('utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        msg = iv + cipher.encrypt(val.encode('utf-8'))
        return binascii.hexlify(msg).decode('utf-8')

    @classmethod
    def decrypt(cls, val, key):
        key = key.encode('utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        return cipher.decrypt(binascii.unhexlify(val))[len(iv):].decode('utf-8')

    @classmethod
    def validate_key(cls, key):
        for s in key:
            if s not in string.ascii_lowercase and s not in string.digits:
                raise ValueError("Lowercase letters and numbers allowed.")

    def validate_password(self, password):
        if len(password) != 16:
            raise ValueError("Password length must be 16, {} found.".format(len(password)))
        if self.notes and self.decrypt(self.notes[self.TEST_KEY], password) != self.TEST_VAL:
            raise ValueError("Invalid password.")

    @classmethod
    def hash_key(cls, key):
        return hashlib.md5(key.encode('utf-8')).hexdigest()[:10]

    def init(self):
        assert not self.notes
        self.notes['keys'] = self.encrypt('', self.password)
        self.notes[self.TEST_KEY] = self.encrypt(self.TEST_VAL, self.password)
        self.save()

    def edit(self, key, value):
        self.validate_key(key=key)
        assert key != self.KEYS_KEY
        assert key != self.TEST_KEY
        keys = set(self.decrypt(self.notes[self.KEYS_KEY], key=self.password).split(','))
        hashed_key = self.hash_key(key)
        initial = ''
        if hashed_key in self.notes:
            initial = self.decrypt(self.notes[hashed_key], key=self.password)
        if key not in keys:
            keys.add(key)
            self.notes[self.KEYS_KEY] = self.encrypt(','.join(keys), key=self.password)
        if value != initial:
            self.notes[hashed_key] = self.encrypt(value, key=self.password)
        self.save()

    def get(self, key):
        encoded_key = self.hash_key(key)
        if encoded_key in self.notes:
            return self.decrypt(self.notes[encoded_key], key=self.password)
        return ''

    def delete(self, key):
        assert key != self.KEYS_KEY
        assert key != self.TEST_KEY
        hashed_key = self.hash_key(key)
        if hashed_key in self.notes:
            del self.notes[hashed_key]
        keys = set(self.decrypt(self.notes[self.KEYS_KEY], key=self.password).split(','))
        if key in keys:
            keys = [k for k in keys if k != key]
            self.notes[self.KEYS_KEY] = self.encrypt(','.join(keys), key=self.password)
        self.save()

    def search(self, prefix):
        keys = set(self.decrypt(self.notes[self.KEYS_KEY], key=self.password).split(','))
        return [k for k in keys if k.startswith(prefix) and k not in (self.TEST_KEY, self.KEYS_KEY)]
