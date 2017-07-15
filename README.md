blurhash-python
===============

Installation
------------
Install blurhash with pip
```
$ pip install blurhash-python
```

Usage
-----
Create blurhash from image file
```python
import blurhash

with open('image.jpg', 'r') as image_file:
    hash = blurhash.encode(image_file, x_components=4, y_components=3)
```
You can also pass file name as parameter to the function
```python
import blurhash

hash = blurhash.encode('image.jpg', x_components=4, y_components=3)
```
Using blurhash with requests
```python
import blurhash
import requests

image_response = requests.get('http://example.com/image.png', stream=True)
hash = blurhash.encode(image_response.raw, x_components=4, y_components=3)
```
`y_components` and `x_components` parameters adjust the amount of
vertical and horizontal AC components in hashed image. Both parameters must
be `>= 1` and `<= 8`.

Build
-----
Build binary distribution
```
$ python setup.py bdist_wheel
```

Build source distribution
```
$ python setup.py sdist
```

See [Python Packaging User Guide](https://packaging.python.org/) for more
information.

Development
-----------
Install development requirements and package in editable mode
```
$ pip install -r dev-requirements.txt
$ pip install -e .
```

Tests
-----
Run test suite with `pytest` in virtual environment
```
$ pytest
```
Use `tox` to run test suite against all supported python versions
```
$ tox
```
