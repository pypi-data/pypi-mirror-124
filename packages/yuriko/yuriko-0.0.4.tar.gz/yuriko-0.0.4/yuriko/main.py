import getpass
import subprocess
import sys
import tempfile

from yuriko import settings
from yuriko.manager import NotesManager
from yuriko.password import gen_password


def editor(initial):
    with tempfile.NamedTemporaryFile() as tf:
        with open(tf.name, 'w') as f:
            f.write(initial)
        subprocess.call(['vim', tf.name])
        with open(tf.name, 'r') as f:
            return f.read()


def main():
    _, command, *arguments = sys.argv

    if command == 'password':
        length = 12
        if arguments:
            length = int(arguments[0])
        print(gen_password(length))
        return

    password = getpass.getpass('Password:')
    password += settings.YURIKO_PASSWORD_SUFFIX
    if len(password) < 16:
        password = (password * 2)
    password = password[:16]

    manager = NotesManager(path=settings.YURIKO_DB_PATH, password=password)

    if command == 'init':
        manager.init()
    elif command == 'search':
        q = arguments[0]
        matches = manager.search(prefix=q)
        for m in matches:
            print("- {}".format(m))
    elif command == 'open':
        key = arguments[0]
        initial = manager.get(key=key)
        value = editor(initial)
        if value != initial:
            manager.edit(key=key, value=value)
    elif command == 'del':
        key = arguments[0]
        manager.delete(key=key)
    else:
        print("Invalid command. Commands available: init, search <prefix>, open <key>, del <key>.")
