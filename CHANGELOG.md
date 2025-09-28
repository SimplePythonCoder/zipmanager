# Changelog

## [0.6.1](https://pypi.org/project/zipmanager/0.6.1/) - 2025-09-28

Added:
- experimental features, you can use the experimental_info function to print a list of them.
- experimental feature that deletes redundant paths in the file_list and the raw zip object.
- wiki function (`from zipmanager import wiki`) will print the docs/wiki url.

Bug fixes:
- fixed some bugs that caused the metadata to not be created.
- fixed issue with create_directory that will allow to create the same directory more than once.

## [0.6.0](https://pypi.org/project/zipmanager/0.6.0/) - 2025-07-03

Added:
- \_\_and__ (as a & b) returns a ZipFolder with all the files that are in both ZipFolder object (Intersection)
- \_\_or__ (as a | b) returns a ZipFolder with all the files that are unique to either ZipFolder object (Symmetric difference)
- \_\_sub__ (as a - b) returns a ZipFolder with files from the first Zipfolder that are not in the second Zipfolder.
- \_\_lshift__ (as a << b) will **copy** all files in other (b) into self (a).
- added safe save that will return an error if the file already exists for both the entire zip and single files.
- added is_folder property to metadata object.
- added `print_csv` to print a csv file as a table.

Updated:
- \_\_add__ (as a + b) will now return a new ZipFolder object.
- markdown functionality and change from `\u001b` to `\033`.
- zipmanager now uses the pyproject.toml instead of setup (it shouldn't affect the installation).

Bug fixes:
- `.csv` files will now use the builtin csv.

## [0.5.2](https://pypi.org/project/zipmanager/0.5.2/) - 2025-03-19

Added:
- support for java and csv files
- \_\_setitem__ (x[y]=z) can now add new files

Bug fixes:
- fixed markdown error when creating bytes

## [0.5.1](https://pypi.org/project/zipmanager/0.5.1/) - 2025-02-10

Added:
- formats
- support for markdown
- str for markdown will have the functions md and print_md

Bug fixes:
- general bug fixes and removal of unnecessary lines

## [0.5.0](https://pypi.org/project/zipmanager/0.5.0/) - 2024-11-15

Added:
- file_hash and zip_hash functions
- set/get_comment for both files and the ZipFolder
- print_zip function to list all files and extra data
- get_creation_datetime to get the file creation time
- create_directory to create empty directories
- \_\_setitem__ (using object['name'] = data)
- save_file to save a specific file

Updated:
- addition, deletion and update functions have been updated for more efficiency
- function names changes:
    - update -> update_file
- list usage for delete_files is now deprecated
- delete_files now returns dict of file names as key and bool if deletion happened successfully

## [0.4.0](https://pypi.org/project/zipmanager/0.4.0/) - 2024-10-14

Added:
  - `update_files` function for multiple file update
  - `change_name` function to change file name
  - `create_base` function to create base files based on extension (`from zipmanager import create_base`)
  - support for html files

Updated:
  - ZipFolder object creation to accept `set` type
  - `add_files` to use `set` type
  - Fixed error in `ZipFolder.__init__` docstring

## [0.3.2](https://pypi.org/project/zipmanager/0.3.2/) - 2024-10-1

- Added `update` function


## [0.3.1](https://pypi.org/project/zipmanager/0.3.1/) - 2024-09-18

- Added `delete_files` function for multiple files

## [0.3.0](https://pypi.org/project/zipmanager/0.3.0/) - 2024-09-12

Added:
- path support
- Added support for py file extension
<details>
<summary>Path examples</summary>

```python
from zipmanager import ZipFolder

ZipFolder('./relative_path/file.zip')
# or
ZipFolder('C:/absolute_path/file.zip')

ZipFolder({'name': './relative_path/file'})
# or
ZipFolder({'name': 'C:/absolute_path/file'})
```
</details>

## [0.2.1](https://pypi.org/project/zipmanager/0.2.1/) - 2024-09-04

- Fixed unsupported data type
- Fixed empty file name
- Fixed base64 error


## [0.2.0](https://pypi.org/project/zipmanager/0.2.0/) - 2024-08-30

Added:
- zip extension support
- Added docstrings to functions

## [0.1.0](https://pypi.org/project/zipmanager/0.1.0/) - 2024-08-27

- First release