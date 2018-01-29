from __future__ import absolute_import
from itertools import chain

from PIL import Image
from six.moves import zip

from ._encode import ffi as _ffi, lib as _lib


__all__ = 'encode',


def encode(image_file, x_components, y_components):
    image = Image.open(image_file).convert('RGB')
    red_band = image.getdata(band=0)
    green_band = image.getdata(band=1)
    blue_band = image.getdata(band=2)
    rgb_data = list(chain.from_iterable(zip(red_band, green_band, blue_band)))
    width, height = image.size
    image.close()

    rgb = _ffi.new('uint8_t[]', rgb_data)
    bytes_per_row = _ffi.cast('size_t', width * 3)
    width = _ffi.cast('int', width)
    height = _ffi.cast('int', height)
    x_components = _ffi.cast('int', x_components)
    y_components = _ffi.cast('int', y_components)

    result = _lib.create_hash_from_pixels(x_components, y_components, width,
                                          height, rgb, bytes_per_row)

    if result == _ffi.NULL:
        raise ValueError('Invalid x_components or y_components')

    return _ffi.string(result)
