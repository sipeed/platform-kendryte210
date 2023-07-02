#include "color.h"

color_t color(uint8_t r, uint8_t g, uint8_t b)
{
    color_t c;

    c.r = (r >= 255) ? 255 : r;
    c.perc_r = (c.r / 255.0);

    c.g = (g >= 255) ? 255 : g;
    c.perc_g = (c.g / 255.0);

    c.b = (b >= 255) ? 255 : b;
    c.perc_b = (c.b / 255.0);

    return c;
}