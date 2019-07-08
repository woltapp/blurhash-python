from __future__ import absolute_import

import pytest

from blurhash import encode


def test_encode_file():
    with open('tests/pic2.png', 'rb') as image_file:
        result = encode(image_file, 4, 3)

    assert result == 'LlMF%n00%#MwS|WCWEM{R*bbWBbH'


def test_encode_with_filename():
    result = encode('tests/pic2.png', 4, 3)
    assert result == 'LlMF%n00%#MwS|WCWEM{R*bbWBbH'


def test_encode_black_and_white_picture():
    result = encode('tests/pic2_bw.png', 4, 3)
    assert result == 'LjIY5?00?bIUofWBWBM{WBofWBj['


def test_invalid_image():
    with pytest.raises(IOError):
        encode('README.md', 4, 3)


def test_file_does_not_exist():
    with pytest.raises(IOError):
        encode('pic404.png', 4, 3)


def test_invalid_x_components():
    with pytest.raises(ValueError):
        encode('tests/pic2.png', 10, 3)

    with pytest.raises(ValueError):
        encode('tests/pic2.png', 0, 3)


def test_invalid_y_components():
    with pytest.raises(ValueError):
        encode('tests/pic2.png', 4, 10)

    with pytest.raises(ValueError):
        encode('tests/pic2.png', 4, 0)
