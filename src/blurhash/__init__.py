from __future__ import absolute_import
from itertools import chain


from PIL import Image

from six.moves import zip

from ._functions import ffi as _ffi, lib as _lib
from ._version import version as __version__


__all__ = 'encode', 'decode', '__version__',

_pixel_modes = {
    "RGB" : 3,
    "RGBA" : 4
}


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

    return _ffi.string(result).decode()

def decode(blurhash, width, height, punch, mode = 'RGB'):

    if not mode in _pixel_modes:
        raise ValueError("Invalid value for argument mode, must be either 'RGB' or 'RGBA'")

    channels = _pixel_modes[mode]

    blurhash_str = _ffi.new('char[]', bytes(blurhash, "utf-8"))

    if not _lib.is_valid_blurhash(blurhash_str) :
        raise ValueError("{} is not a valid blurhash".format(blurhash))

    width_int = _ffi.cast('int', width)
    height_int = _ffi.cast('int', height)
    punch_int = _ffi.cast('int', punch)
    channels_int = _ffi.cast('int', channels)

    pixels = _lib.create_pixels_from_blurhash(blurhash_str, width_int, height_int,
                                    punch_int, channels)
    
    if pixels == _ffi.NULL :
        raise Exception("Failed to decode blurhash {}".format(blurhash))

    #garbage collection of pixel buffer
    pixels = _ffi.gc(pixels, _lib.free_pixel_array)

    pixels_buffer = _ffi.buffer(pixels, width * height * channels)

    image = Image.frombuffer(mode, (width, height), pixels_buffer)

    return image

def is_valid_blurhash(blurhash) :

    blurhash_str = _ffi.new('char[]', bytes(blurhash, 'utf-8'))
    return bool(_lib.is_valid_blurhash(blurhash_str))
