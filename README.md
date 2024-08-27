# zipmanager
```
pip install zipmanager
```
## What does this package do ?
It allows you to create and handle zip folders as data without needing to save them.

## Usage
```python
from zipmanager import ZipFolder

file_data = b'some_data'

zip_folder = ZipFolder({'file_name.file_extension': file_data})
# file extension not required
# ZipFile will hold all the files given in the dictionary

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

## File extension features
json and text files data is automatically returned as a dict or str respectively:
```python
from zipmanager import ZipFolder

file_data = b'{"key": "value"}'

zip_folder = ZipFolder({'file_name.json': file_data})
# .json extension is required to return a dict

data = zip_folder['file_name.json']
# will return a dict type

# same for .txt
file_data = {'key': 'value'}
zip_folder = ZipFolder({'file_name.txt': file_data})
data = zip_folder['file_name.txt']
# will return a string
```