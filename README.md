# zipmanager
[![downloads](https://static.pepy.tech/badge/zipmanager)](https://www.pepy.tech/projects/zipmanager) [![changelog](https://raw.githubusercontent.com/SimplePythonCoder/zipmanager/main/images/Changelog.svg)](https://github.com/SimplePythonCoder/zipmanager/blob/main/CHANGELOG.md) [![wiki](https://raw.githubusercontent.com/SimplePythonCoder/zipmanager/main/images/Wiki.svg)](https://github.com/SimplePythonCoder/zipmanager/wiki)
```
pip install zipmanager
```
## What does this package do ?
It allows you to create and handle zip folders as data without needing to save them.

## Usage
```python
from zipmanager import ZipFolder

file_data = b'some data'

zip_folder = ZipFolder({'file_name.file_extension': file_data})
# file extension not required
# ZipFolder will hold all the files given in the dictionary

file_data = zip_folder['file_name.file_extension']
# will return the file data
```

## Main functions
```python
from zipmanager import ZipFolder

file_data = b'some_data'
zip_folder = ZipFolder({'file_name.file_extension': file_data})

# list of functions:
zip_folder.add_files({'new_file': 'new_data'}) # add files to zip. read more at docstring.
zip_folder.delete_file('new_file') # removes file from zip

zip_folder.get('file_name') # returns None if file was not found
# or
zip_folder['file_name']

zip_folder.save() # saves zip in given location (empty is './temp.zip')
```

## Features
info on more of the features is available on the [wiki](https://github.com/SimplePythonCoder/zipmanager/wiki)