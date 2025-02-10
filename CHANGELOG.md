# Changelog

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
- \__setitem\__ (using object['name'] = data)
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