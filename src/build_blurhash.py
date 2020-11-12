from __future__ import absolute_import

import cffi
import sys


ffibuilder = cffi.FFI()
ffibuilder.set_source('blurhash._functions', '''

    const char* blurHashForPixels(int x_components, int y_components, int width, int height,
                                uint8_t * rgb, size_t bytesPerRow);
    uint8_t * decode(const char* blurhash, int width, int height, int punch, int n_channels);
    void freePixelArray(uint8_t * pixelsPtr);
    

    const char* create_hash_from_pixels(int x_components, int y_components,
                                       int width, int height, uint8_t* rgb,
                                       size_t bytes_per_row) {
        return blurHashForPixels(x_components, y_components, width, height,
                                 rgb, bytes_per_row);
    }

    uint8_t * create_pixels_from_blurhash(const char * blurhash, int width, int height, 
                                     int punch, int n_channels){
            return decode(blurhash, width, height, punch, n_channels);
    }

    int is_valid_blurhash(const char * blurhash) {
        return isValidBlurhash(blurhash);
    }

    void free_pixel_array(uint8_t * pixel_ptr) {
        freePixelArray(pixel_ptr);
    }
''', sources=['src/encode.c', 'src/decode.c'], extra_compile_args=['-std=gnu99'] if sys.platform != 'win32' else [])

ffibuilder.cdef('''
    const char* create_hash_from_pixels(int x_components, int y_components,
                                       int width, int height, uint8_t* rgb,
                                       size_t bytes_per_row);
    uint8_t * create_pixels_from_blurhash(const char * blurhash, int width, int height,
                                    int punch, int nChannels);

    int is_valid_blurhash(const char * blurhash);
    
    void free_pixel_array(uint8_t * pixel_ptr);
''')


if __name__ == '__main__':
    ffibuilder.compile()
