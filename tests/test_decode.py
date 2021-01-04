from __future__ import absolute_import

import pytest

from PIL import Image
from blurhash import decode, PixelMode


def test_decode_blurhash():
    image = decode("LlMF%n00%#MwS|WCWEM{R*bbWBbH", 416, 416)
    assert type(image) == Image.Image


def test_decode_rgba():
    image = decode("LlMF%n00%#MwS|WCWEM{R*bbWBbH", 416, 416,
                   mode=PixelMode.RGBA)

    assert image.getbands() == ('R', 'G', 'B', 'A')


def test_decode_rgb():
    image = decode("LlMF%n00%#MwS|WCWEM{R*bbWBbH", 416, 416,
                   mode=PixelMode.RGB)
    assert image.getbands() == ('R', 'G', 'B')


def test_decode_punch():
    image = decode("LlMF%n00%#MwS|WCWEM{R*bbWBbH", 416, 416, punch=2)
    assert type(image) == Image.Image


def test_decode_invalid_blurhash():
    with pytest.raises(ValueError):
        decode("#MwS|WCWEM{R", 416, 416)


def test_decode_invalid_mode():
    with pytest.raises(ValueError):
        decode("LlMF%n00%#MwS|WCWEM{R*bbWBbH", 416, 416, mode='XXX')


def test_decode_invalid_width():
    with pytest.raises(ValueError):
        decode("LlMF%n00%#MwS|WCWEM{R*bbWBbH", -416, 416)


def test_decode_invalid_height():
    with pytest.raises(ValueError):
        decode("LlMF%n00%#MwS|WCWEM{R*bbWBbH", 416, 0)


def test_decode_invalid_punch():
    with pytest.raises(ValueError):
        decode("LlMF%n00%#MwS|WCWEM{R*bbWBbH", 416, 416, punch=-2)


def test_decode_valid_width_height():
    image = decode("LlMF%n00%#MwS|WCWEM{R*bbWBbH", 640, 480)
    assert (image.width == 640 and image.height == 480)
