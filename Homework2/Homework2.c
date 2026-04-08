#include <stdio.h> // set pico_enable_stdio_usb to 1 in CMakeLists.txt 
#include "pico/stdlib.h" // CMakeLists.txt must have pico_stdlib in target_link_libraries
#include "hardware/pwm.h" // CMakeLists.txt must have hardware_pwm in target_link_libraries
#include "hardware/adc.h" // CMakeLists.txt must have hardware_adc in target_link_libraries

void set_servo_angle(int angle);

#define PWMPIN 16

int main()
{
    // turn on usb and initalize variables
    stdio_init_all(); 

     // turn on the pwm 
    gpio_set_function(PWMPIN, GPIO_FUNC_PWM); // Set the Pin to be PWM
    uint slice_num = pwm_gpio_to_slice_num(PWMPIN); // Get PWM slice number
    // the clock frequency is 150MHz divided by a float from 1 to 255
    float div = 50; // must be between 1-255
    pwm_set_clkdiv(slice_num, div); // sets the clock speed
    uint16_t wrap = 60000; // when to rollover, must be less than 65535
    // set the PWM frequency and resolution
    // this sets the PWM frequency to 150MHz/div/wrap
    pwm_set_wrap(slice_num, wrap); 
    pwm_set_enabled(slice_num, true); // turn on the PWM

    while (true) {

        //Sweep forward (0 → 180)
        for (int angle=0; angle <= 180; angle++)
        {
            set_servo_angle(angle);
            sleep_ms(10);
        }
        
        // Sweep backward (180 → 0)
        for (int angle=180; angle >= 0; angle--)
        {
            set_servo_angle(angle);
            sleep_ms(10);
        }

    }

}

void set_servo_angle(int angle){
    pwm_set_gpio_level(PWMPIN, (int)((0.02 + (angle/180.0)*0.1)*60000));
}