#include <stdio.h>

#include "pico/stdlib.h"

#include "hardware/i2c.h"
#include "hardware/adc.h"
#include "hardware/timer.h"

#include "ssd1306.h"
#include "mpu6050.h"
#include "font.h"

// I2C pins
#define I2C_PORT i2c0
#define I2C_SDA 4
#define I2C_SCL 5
#define LED_PIN 15 

// Introduce functions
void blinkLED();

int main(){

    stdio_init_all();

    // I2C Initialisation. Using it at 400Khz.
    i2c_init(I2C_PORT, 400*1000);
    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C); // assign SDA pin to I2C
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C); // assign SCL pin to I2C
    
    // Intialize LED 
    gpio_init(LED_PIN);              // initialize pin
    gpio_set_dir(LED_PIN, GPIO_OUT); // set as output

    // Initalize display
    ssd1306_setup();

    // IMU Initalization
    init_mpu6050();   // turn on the IMU
    uint8_t data[14];
    uint8_t who = whoami();    

    if (who !=0x68 && who!=0x98){    // Check if IMU is not found
        while(1){
            gpio_put(LED_PIN, 1);    // Turn LED ON
        }
    }

    // Proceed...
    while (true){
        blinkLED();

        // Read from IMU
        burst_read_mpu6050(data);

        // Convert x and y acc.
        float ax = conv_xXL(data);
        float ay = conv_yXL(data);

        // Set screen center & scale for lines
        int xc = 64;
        int yc = 16;

        float scale = 20.0;

        // Calculate x & y, draw vectors
        int x = xc - (int)(ax * scale);
        int y = yc + (int)(ay * scale);  // invert Y

        ssd1306_clear();

        ssd1306_drawLine(xc, yc, x, yc, 1); // draw X line
        ssd1306_drawLine(xc, yc, xc, y, 1); // draw Y line
        ssd1306_drawPixel(xc, yc, 1);       // draw center

        ssd1306_update();

    }
}

// Heartbeat LED
void blinkLED(){

    int on = 1;
    int off = 0;

    // Turn on LED
    gpio_put(LED_PIN, on);
    sleep_ms(10);

    // Turn off LED
    gpio_put(LED_PIN, off);
    sleep_ms(10);
}