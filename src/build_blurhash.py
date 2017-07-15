from __future__ import absolute_import

import cffi


ffibuilder = cffi.FFI()
ffibuilder.set_source('blurhash._encode', '''
    const char* blurHashForPixels(int xComponents, int yComponents, int width,
                                  int height, uint8_t *rgb,
                                  size_t bytesPerRow);

    const char* create_hash_from_pixels(int x_components, int y_components,
                                       int width, int height, uint8_t* rgb,
                                       size_t bytes_per_row) {
        return blurHashForPixels(x_components, y_components, width, height,
                                 rgb, bytes_per_row);
    }
''', sources=['src/encode.c'])
ffibuilder.cdef('''
    const char* create_hash_from_pixels(int x_components, int y_components,
                                       int width, int height, uint8_t* rgb,
                                       size_t bytes_per_row);
''')

if __name__ == '__main__':
    ffibuilder.compile()
