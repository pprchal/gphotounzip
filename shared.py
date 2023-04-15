import hashlib

IGNORED_GOOGLE_FOLDERS = ['/Koš/']
BUFFER_SIZE = 4096
IGNORED_DEST = ["@eaDir", "@SynoEAStream", "SYNOINDEX_", "SYNOPHOTO_"]

def is_ignored(path, ignored):
    return any(ignored in path for ignored in ignored)

def get_file_hash(file):
    hash_obj = hashlib.sha1()
    while True:
        data = file.read(BUFFER_SIZE)
        if not data:
            break
        hash_obj.update(data)
    return format(hash_obj.hexdigest())

