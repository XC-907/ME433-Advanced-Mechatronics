#include <stdlib.h>
#include <stdio.h> // set pico_enable_stdio_usb to 1 in CMakeLists.txt 
#include "pico/stdlib.h" // CMakeLists.txt must have pico_stdlib in target_link_libraries
#include "mpu6050.h"
#include "hardware/i2c.h"
#include <math.h>

// I2C pins
#define I2C_PORT i2c0
#define I2C_SDA 4
#define I2C_SCL 5

#define TILT_THRESHOLD 0.1

int main()
{
    stdio_init_all();

    // I2C and IMU Initalization
    i2c_init(I2C_PORT, 400000);
    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C); // assign SDA pin to I2C
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C); // assign SCL pin to I2C

    init_mpu6050();

    uint8_t data[14];;

    while (true) {
        burst_read_mpu6050(data);

        float ax = conv_xXL(data);  // tilt left/right
        float ay = conv_yXL(data);  // tilt forward/back

        printf("(%.3f,%.3f)\n", ax, ay);

        sleep_ms(1000/60);  // update at 30Hz
    }
}