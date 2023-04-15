import sys
import os
import shared

def get_disk_hash(path):
    with open(path, "rb") as file:
        return shared.get_file_hash(file)

def hash_directories(directory):
    if shared.is_ignored(directory, shared.IGNORED_DEST):
        return
    
    # print progress
    sys.stderr.write(f'{directory}\n')

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if shared.is_ignored(filepath, shared.IGNORED_DEST):
            continue
        elif os.path.isfile(filepath):
            file_hash = get_disk_hash(filepath)
            print(f'SHA1:{file_hash} {filepath}')
        elif os.path.isdir(filepath):
            hash_directories(filepath)

if len(sys.argv) != 2:
    print('Hash file name missing')

hash_directories(sys.argv[1])

