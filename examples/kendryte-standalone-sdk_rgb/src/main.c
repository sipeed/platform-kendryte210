
/* Author: Fabrice Beya
 *
 * This sample demo configures the onboard RGB LED's M1W Dock. The LED's are attached to 3 PWM channels on Timer 1.
 * Various colors are set based on the traditional rgb metric(values 0-255) which are mapped to the pwn duty
 * cycles for each LED.
 */

#include <stdio.h>
#include <unistd.h>
#include <syslog.h>
#include <timer.h>
#include <pwm.h>
#include <fpioa.h>
#include "color.h"

#define LED_G 12
#define LED_R 13
#define LED_B 14

#define TIMER_DEV_NUM       TIMER_DEVICE_1
#define LED_R_TIMER_CHN     TIMER_CHANNEL_0
#define LED_G_TIMER_CHN     TIMER_CHANNEL_1
#define LED_B_TIMER_CHN     TIMER_CHANNEL_2

#define FREQ                1000

color_t WHITE = { 255, 255, 255, 1, 1, 1 };
color_t BLACK = { 0, 0, 0, 0, 0, 0 };
color_t RED = { 255, 0, 0, 1, 0 , 0};
color_t GREEN = { 0, 255, 0, 0, 1, 0 };
color_t BLUE = { 0, 0, 255, 0, 0, 1 };

void set_color(color_t color)
{
    printf("Updating rgb with values: R:%d G:%d B:%d\n", color.r, color.g, color.b);
    printf("Updating duty cycle with values: R:%f G:%f B:%f\n", color.perc_r, color.perc_g, color.perc_b);
    
    /* Update duty cycle for each LED channel. */
    pwm_set_frequency(TIMER_DEV_NUM, LED_R_TIMER_CHN, FREQ, (1 - color.perc_r));
    pwm_set_frequency(TIMER_DEV_NUM, LED_G_TIMER_CHN, FREQ, (1 - color.perc_g));
    pwm_set_frequency(TIMER_DEV_NUM, LED_B_TIMER_CHN, FREQ, (1 - color.perc_b));
}

int main()
{
    LOGI(__func__, "RGB Demo "__DATE__ " " __TIME__);

    /* Init FPIOA pin mapping for RGB pins to be driver by PWM*/
    fpioa_set_function(LED_R, FUNC_TIMER1_TOGGLE2);
    fpioa_set_function(LED_G, FUNC_TIMER1_TOGGLE3);
    fpioa_set_function(LED_B, FUNC_TIMER1_TOGGLE1);

    /* Init PWM */
    pwm_init(TIMER_DEV_NUM);

    /* Set RGB to white */
    set_color(WHITE);

    /* Enable PWM's */
    pwm_set_enable(TIMER_DEV_NUM, LED_R_TIMER_CHN, 1);
    pwm_set_enable(TIMER_DEV_NUM, LED_G_TIMER_CHN, 1);
    pwm_set_enable(TIMER_DEV_NUM, LED_B_TIMER_CHN, 1);
    
    /* Create custom color by passing in rgb values */
    color_t PURPLE = color(190, 15, 209);

    while(1)
    {
        /* Cycle through a sequence of Red -> Green -> Blue -> PURPLE -> White -> Black in 1 second phases. */
        set_color(RED); 
        sleep(1);
        set_color(GREEN);
        sleep(1);
        set_color(BLUE); 
        sleep(1);
        set_color(PURPLE);
        sleep(1);
        set_color(WHITE);
        sleep(1);
        set_color(BLACK);
        sleep(1);
    }

    return 0;
}