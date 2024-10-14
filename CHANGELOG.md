# Changelog

## [0.4.0](https://pypi.org/project/zipmanager/0.4.0/) - 2024-10-14

- Added `update_files` function for multiple file update
- Added `change_name` function to change file name
- Added `create_base` function to create base files based on extension (`from zipmanager import create_base`)
- Added support for html files
- Updated ZipFolder object creation to accept `set` type
- Updated `add_files` to use `set` type
- Fixed error in `ZipFolder.__init__` docstring

## [0.3.2](https://pypi.org/project/zipmanager/0.3.2/) - 2024-10-1

- Added `update` function


## [0.3.1](https://pypi.org/project/zipmanager/0.3.1/) - 2024-09-18

- Added `delete_files` function for multiple files

## [0.3.0](https://pypi.org/project/zipmanager/0.3.0/) - 2024-09-12

- Added path support
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

- Added zip extension support
- Added docstrings to functions

## [0.1.0](https://pypi.org/project/zipmanager/0.1.0/) - 2024-08-27

- First release