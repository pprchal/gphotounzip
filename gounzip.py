import zipfile
import sys
import os
import shared

class rec:
    def __init__(self, hash, path):
        self.sha = hash
        self.path = path

def load_sha1(shafile):
    with open(shafile, "r") as f:
        lines = f.readlines()
        for line in lines:
            hash = line[5:44]
            path = line[46:].strip()
            yield rec(hash, path)

def find_by_sha1(sha):
    for rec in database:
        if rec.sha == sha:
            yield rec

def copy_file(zip_file, file_path):
    if os.path.exists(file_path):
        print(f'- {file_path} already exists (by name)')
        return

    # ensure, that dir is exists. if no, create
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    zip_file.seek(0, 0)
    size = 0
    with open(file_path, 'wb') as dest_file:
        while True:
            data = zip_file.read(shared.BUFFER_SIZE)
            size = size + len(data)
            if not data:
                break
            else:
                dest_file.write(data)

    print(f'+ {file_path} ({size/1024:.2f}k) copied')


def unpack_zip(zip_path, dest_folder):
    with zipfile.ZipFile(zip_path, 'r') as zip_archive:
        for zip_file_name in zip_archive.namelist():
            # ignore google metadata files
            if zip_file_name.endswith('.json'):
                continue
            if shared.is_ignored(dest_file_name, shared.IGNORED_GOOGLE_FOLDERS):
                continue

            # process file from zip arc
            with zip_archive.open(zip_file_name, 'r') as zip_file:
                dest_file_name = zip_file_name[21:] # Takeout/Fotky Google


                file_path = os.path.join(dest_folder, dest_file_name)
                zip_file_hash = shared.get_file_hash(zip_file)
                duplicates = list(find_by_sha1(zip_file_hash))

                if len(duplicates) > 0:
                    # print dups
                    print(f'ZIP file: {zip_file_name} is {len(duplicates)}x dup:')
                    for dup in duplicates:
                        print(f'\t{dup.path}')
                else:
                    # update db
                    database.append(rec(hash=zip_file_hash, path=file_path))
                    copy_file(zip_file, file_path)

# parse inputs
DATABASE_FILE = sys.argv[1]
ZIP_FILE = sys.argv[2]
DEST_FOLDER = sys.argv[3]

# load db
database = list(load_sha1(DATABASE_FILE))
print(f'Hash DB loaded:{DATABASE_FILE}, {len(database)} record(s)')

# rozbal soubory
unpack_zip(ZIP_FILE, DEST_FOLDER)


