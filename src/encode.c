#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "common.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

struct RGB {
	float r;
	float g;
	float b;
};

static struct RGB multiplyBasisFunction(int xComponent, int yComponent, int width, int height, uint8_t *rgb, size_t bytesPerRow);
static char *encode_int(int value, int length, char *destination);

static int encodeDC(float r, float g, float b);
static int encodeAC(float r, float g, float b, float maximumValue);

const char *blurHashForPixels(int xComponents, int yComponents, int width, int height, uint8_t *rgb, size_t bytesPerRow, char *destination) {
	if(xComponents < 1 || xComponents > 9) return NULL;
	if(yComponents < 1 || yComponents > 9) return NULL;

#ifndef _MSC_VER
	float factors[yComponents * xComponents][3];
#else
	float factors[9 * 9][3];
#endif
	memset(factors, 0, sizeof(factors));

	for(int y = 0; y < yComponents; y++) {
		for(int x = 0; x < xComponents; x++) {
			struct RGB factor = multiplyBasisFunction(x, y, width, height, rgb, bytesPerRow);
			factors[y * xComponents + x][0] = factor.r;
			factors[y * xComponents + x][1] = factor.g;
			factors[y * xComponents + x][2] = factor.b;
		}
	}

	float *dc = factors[0];
	float *ac = dc + 3;
	int acCount = xComponents * yComponents - 1;
	char *ptr = destination;

	int sizeFlag = (xComponents - 1) + (yComponents - 1) * 9;
	ptr = encode_int(sizeFlag, 1, ptr);

	float maximumValue;
	if(acCount > 0) {
		float actualMaximumValue = 0;
		for(int i = 0; i < acCount * 3; i++) {
			actualMaximumValue = fmaxf(fabsf(ac[i]), actualMaximumValue);
		}

		int quantisedMaximumValue = fmaxf(0, fminf(82, floorf(actualMaximumValue * 166 - 0.5)));
		maximumValue = ((float)quantisedMaximumValue + 1) / 166;
		ptr = encode_int(quantisedMaximumValue, 1, ptr);
	} else {
		maximumValue = 1;
		ptr = encode_int(0, 1, ptr);
	}

	ptr = encode_int(encodeDC(dc[0], dc[1], dc[2]), 4, ptr);

	for(int i = 0; i < acCount; i++) {
		ptr = encode_int(encodeAC(ac[i * 3 + 0], ac[i * 3 + 1], ac[i * 3 + 2], maximumValue), 2, ptr);
	}

	*ptr = 0;

	return destination;
}

static struct RGB multiplyBasisFunction(int xComponent, int yComponent, int width, int height, uint8_t *rgb, size_t bytesPerRow) {
	struct RGB result = { 0, 0, 0 };
	float normalisation = (xComponent == 0 && yComponent == 0) ? 1 : 2;

	for(int y = 0; y < height; y++) {
		for(int x = 0; x < width; x++) {
			float basis = cosf(M_PI * xComponent * x / width) * cosf(M_PI * yComponent * y / height);
			result.r += basis * sRGBToLinear(rgb[3 * x + 0 + y * bytesPerRow]);
			result.g += basis * sRGBToLinear(rgb[3 * x + 1 + y * bytesPerRow]);
			result.b += basis * sRGBToLinear(rgb[3 * x + 2 + y * bytesPerRow]);
		}
	}

	float scale = normalisation / (width * height);

	result.r *= scale;
	result.g *= scale;
	result.b *= scale;

	return result;
}

static int encodeDC(float r, float g, float b) {
	int roundedR = linearTosRGB(r);
	int roundedG = linearTosRGB(g);
	int roundedB = linearTosRGB(b);
	return (roundedR << 16) + (roundedG << 8) + roundedB;
}

static int encodeAC(float r, float g, float b, float maximumValue) {
	int quantR = fmaxf(0, fminf(18, floorf(signPow(r / maximumValue, 0.5) * 9 + 9.5)));
	int quantG = fmaxf(0, fminf(18, floorf(signPow(g / maximumValue, 0.5) * 9 + 9.5)));
	int quantB = fmaxf(0, fminf(18, floorf(signPow(b / maximumValue, 0.5) * 9 + 9.5)));

	return quantR * 19 * 19 + quantG * 19 + quantB;
}

static char characters[83]="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%*+,-.:;=?@[]^_{|}~";

static char *encode_int(int value, int length, char *destination) {
	int divisor = 1;
	for(int i = 0; i < length - 1; i++) divisor *= 83;

	for(int i = 0; i < length; i++) {
		int digit = (value / divisor) % 83;
		divisor /= 83;
		*destination++ = characters[digit];
	}
	return destination;
}
