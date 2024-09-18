# Changelog

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