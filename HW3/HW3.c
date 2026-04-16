#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

// I2C pins
#define I2C_PORT i2c0
#define I2C_SDA 4
#define I2C_SCL 5

int main() {

    stdio_init_all();
    sleep_ms(500); // give terminal time to connect

    printf("Booting...\n");

    // I2C Initialization. Using it at 400Khz.
    i2c_init(I2C_PORT, 400 * 1000);
    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C);
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C);

    gpio_pull_up(I2C_SDA);
    gpio_pull_up(I2C_SCL);

    while (true) {

        printf("Scanning...\n");

        int found = 0;

        for (int addr = 0; addr < 128; addr++) {

            int result = i2c_write_blocking(I2C_PORT, addr, NULL, 0, false);

            if (result >= 0) {
                printf("Found device at 0x%02X\n", addr);
                found++;
            }
        }

        if (found == 0) {
            printf("No devices found\n");
        }

        printf("Scan done\n\n");

        sleep_ms(500);
    }
}