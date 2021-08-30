#include <math.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#include "common.h"

static char chars[83] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%*+,-.:;=?@[]^_{|}~";

static inline uint8_t clampToUByte(int src) {
	if (src >= 0 && src <= 255) {
		return src;
	} else if (src < 0) {
		return 0;
	} else {
		return 255;
	}
}

static inline uint8_t *  createByteArray(int size) {
	return (uint8_t *)malloc(size * sizeof(uint8_t));
}

int decodeToInt(const char * string, int start, int end) {
	int value = 0;
	for (int iter1 = start; iter1 < end; iter1 ++) {
		int index = -1;
		for (int iter2 = 0; iter2 < 83; iter2 ++) {
			if (chars[iter2] == string[iter1]) {
				index = iter2;
				break;
			}
		}

		if (index == -1) {
			return -1;
		}

		value = value * 83 + index;
	}
	return value;
}

bool isValidBlurhash(const char * blurhash) {
	const int hashLength = strlen(blurhash);

	if (!blurhash || strlen(blurhash) < 6) {
		return false;
	}

	int sizeFlag = decodeToInt(blurhash, 0, 1);	//Get size from first character
	int numY = (sizeFlag / 9) + 1;
	int numX = (sizeFlag % 9) + 1;

	if (hashLength != 4 + 2 * numX * numY) {
		return false;
	}

	return true;
}

void decodeDC(int value, float * r, float * g, float * b) {
	*r = sRGBToLinear(value >> 16); 	// R-component
	*g = sRGBToLinear((value >> 8) & 255); // G-Component
	*b = sRGBToLinear(value & 255);	// B-Component
}

void decodeAC(int value, float maximumValue, float * r, float * g, float * b) {
	int quantR = value / (19 * 19);
	int quantG = (value / 19) % 19;
	int quantB = value % 19;

	*r = signPow(((float)quantR - 9.0) / 9.0, 2.0) * maximumValue;
	*g = signPow(((float)quantG - 9.0) / 9.0, 2.0) * maximumValue;
	*b = signPow(((float)quantB - 9.0) / 9.0, 2.0) * maximumValue;
}

int decodeToArray(const char * blurhash, int width, int height, int punch, int nChannels, uint8_t * pixelArray) {
	if (!isValidBlurhash(blurhash)) {
		return -1;
	}

	if (punch < 1) {
		punch = 1;
	}

	int sizeFlag = decodeToInt(blurhash, 0, 1);
	int numY = (sizeFlag / 9) + 1;
	int numX = (sizeFlag % 9) + 1;

	float r = 0, g = 0, b = 0;
	int quantizedMaxValue = decodeToInt(blurhash, 1, 2);
	if (quantizedMaxValue == -1) {
		return -1;
	}

	float maxValue = ((float)(quantizedMaxValue + 1.0)) / 166.0;

	int colors_size = numX * numY;
	float* colors = malloc(colors_size * 3 * sizeof(float));

	for (int iter = 0; iter < colors_size; iter++) {
		if (iter == 0) {
			int value = decodeToInt(blurhash, 2, 6);
			if (value == -1) {
				free(colors);
				return -1;
			}

			decodeDC(value, &r, &g, &b);
			colors[3 * iter + 0] = r;
			colors[3 * iter + 1] = g;
			colors[3 * iter + 2] = b;

		} else {
			int value = decodeToInt(blurhash, 4 + iter * 2, 6 + iter * 2);
			if (value == -1) {
				free(colors);
				return -1;
			}

			decodeAC(value, maxValue * punch, &r, &g, &b);
			colors[3 * iter + 0] = r;
			colors[3 * iter + 1] = g;
			colors[3 * iter + 2] = b;
		}
	}

	int bytesPerRow = width * nChannels;

	for (int y = 0; y < height; y++) {
		for (int x = 0; x < width; x++) {

			float r = 0, g = 0, b = 0;

			for (int j = 0; j < numY; j ++) {
				for (int i = 0; i < numX; i ++) {
					float basics = cos((M_PI * x * i) / width) * cos((M_PI * y * j) / height);
					int idx = i + j * numX;
					r += colors[3 * idx + 0] * basics;
					g += colors[3 * idx + 1] * basics;
					b += colors[3 * idx + 2] * basics;
				}
			}

			int intR = linearTosRGB(r);
			int intG = linearTosRGB(g);
			int intB = linearTosRGB(b);

			pixelArray[nChannels * x + 0 + y * bytesPerRow] = clampToUByte(intR);
			pixelArray[nChannels * x + 1 + y * bytesPerRow] = clampToUByte(intG);
			pixelArray[nChannels * x + 2 + y * bytesPerRow] = clampToUByte(intB);

			if (nChannels == 4) {
				pixelArray[nChannels * x + 3 + y * bytesPerRow] = 255;   // If nChannels=4, treat each pixel as RGBA instead of RGB
			}
		}
	}

	free(colors);

	return 0;
}

uint8_t * decode(const char * blurhash, int width, int height, int punch, int nChannels) {
	int bytesPerRow = width * nChannels;
	uint8_t * pixelArray = createByteArray(bytesPerRow * height);

	if (decodeToArray(blurhash, width, height, punch, nChannels, pixelArray) == -1) {
		return NULL;
	}

	return pixelArray;
}

void freePixelArray(uint8_t * pixelArray) {
	if (pixelArray) {
		free(pixelArray);
	}
}
