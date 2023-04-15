# gphotounzip
> Five minutes solution

> Unzip google backup `.zip` to directory skipping duplicates.

1. create hash db `python create.py ~/path/to/photos > photos.sha1`
2. unpack zip `python gounzip.py photos.sha1 takeout_google.zip ~/path/to/photos`

> TIP: Modify `shared.py` - skip patterns, etc...
