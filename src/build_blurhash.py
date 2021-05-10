from __future__ import absolute_import

import cffi
import sys


ffibuilder = cffi.FFI()
ffibuilder.set_source('blurhash._functions', '''
    #include <stdbool.h>

    #include "common.h"

    const char* blurHashForPixels(int x_components, int y_components,
                                  int width, int height,
                                  uint8_t * rgb, size_t bytesPerRow);

    int decodeToArray(const char* blurhash, int width, int height,
                      int punch, int n_channels,
                      uint8_t * pixel_array);

    bool isValidBlurhash(const char* blurhash);


    const char* create_hash_from_pixels(int x_components, int y_components,
                                        int width, int height, uint8_t* rgb,
                                        size_t bytes_per_row) {
        return blurHashForPixels(x_components, y_components, width, height,
                                 rgb, bytes_per_row);
    }

    int create_pixels_from_blurhash(const char * blurhash, int width,
                                    int height, int punch, int n_channels,
                                    uint8_t * pixel_array){
        return decodeToArray(blurhash, width, height,
                             punch, n_channels, pixel_array);
    }

    int is_valid_blurhash(const char * blurhash) {
        return isValidBlurhash(blurhash);
    }
''', sources=['src/encode.c', 'src/decode.c'],
        include_dirs=['src/'],
        extra_compile_args=['-std=gnu99'] if sys.platform != 'win32' else []
    )

ffibuilder.cdef('''
    const char* create_hash_from_pixels(int x_components, int y_components,
                                        int width, int height, uint8_t* rgb,
                                        size_t bytes_per_row);
    int create_pixels_from_blurhash(const char * blurhash, int width,
                                    int height, int punch, int nChannels,
                                    uint8_t * pixel_array);

    int is_valid_blurhash(const char * blurhash);

''')


if __name__ == '__main__':
    ffibuilder.compile()
