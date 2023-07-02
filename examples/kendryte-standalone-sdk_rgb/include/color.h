#ifndef __COLOR__
#define __COLOR__
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
    double perc_r;
    double perc_g;
    double perc_b;
} color_t;

color_t color(uint8_t r, uint8_t g, uint8_t b);
#endif