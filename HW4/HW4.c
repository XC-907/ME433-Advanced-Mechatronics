#include <stdio.h>
#include "pico/stdlib.h"

#include "hardware/i2c.h"
#include "hardware/adc.h"
#include "hardware/timer.h"

#include "ssd1306.h"
#include "font.h"

// I2C pins
#define I2C_PORT i2c0
#define I2C_SDA 4
#define I2C_SCL 5
#define LED_PIN 15 

void ssd1306_drawChar(int x, int y, char c);
void ssd1306_drawMessage(int x, int y, char *message);
void blink_LED(int i);

int main()
{
    stdio_init_all();

    // I2C Initialization. Using it at 400Khz.
    i2c_init(I2C_PORT, 400*1000);
    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C); // assign SDA pin to I2C
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C); // assign SCL pin to I2C
    
    // Intialize LED 
    gpio_init(LED_PIN);              // initialize pin
    gpio_set_dir(LED_PIN, GPIO_OUT); // set as output

    // Initalize ADC
    adc_init();
    adc_gpio_init(26);
    adc_select_input(0);
    
    // Initalize display
    ssd1306_setup();

    // Get current time
    unsigned int prev_time = to_us_since_boot(get_absolute_time());

    while (true) {

        // Heartbeat LED
        blink_LED(1);
        sleep_ms(10);
        blink_LED(0);
        sleep_ms(10);

        // Calculate FPS
        unsigned int time_now = to_us_since_boot(get_absolute_time());
        float dt = (time_now - prev_time) / 1000000.0f;
        prev_time = time_now;

        float fps = 1.0f/ dt;

        // Determine & convert ADC voltage
        uint16_t adc_raw = adc_read();
        float voltage = adc_raw * 3.3f / 4095.0f;

        // Draw on display
        ssd1306_clear();                // clear screen buffer

        char line1[50];                 // Character array for line 1
        char line2[50];                 // Character array for line 2
        
        sprintf(line1, "Voltage of AC0 = %.2f V", voltage); 
        sprintf(line2, "FPS = %.2f frames/s", fps);

        ssd1306_drawMessage(0, 0, line1);    
        ssd1306_drawMessage(0, 8, line2);  

        ssd1306_update();               // send to display
    }
}

void blink_LED(int i){
    gpio_put(LED_PIN, i);
}

void ssd1306_drawChar(int x, int y, char c) {
    
    // Loop through columns
    for (int j=0; j <5; j++){
        // Loop through rows
        for(int k=0; k <8; k++){

            // Extract pixel value (i.e. on or off)
            int pixel = (ASCII[c - 0x20][j] >> k) & 1;

            // Draw that pixel
            ssd1306_drawPixel(x+j, y+k, pixel);       
        }  
    }
}

void ssd1306_drawMessage(int x, int y, char *message){
    // Start at first char
    int s = 0;

    // Loop through the message
    while (message[s]!=0){
        ssd1306_drawChar(x, y, message[s]);
        // move right for the next char 
        // (add a little extra space so letters aren't as close)
        x += 6;    
        s++;
    }
}