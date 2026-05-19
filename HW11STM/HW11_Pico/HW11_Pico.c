#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/uart.h"

// UART defines
#define UART_ID uart0
#define BAUD_RATE 115200

#define UART_TX_PIN 0
#define UART_RX_PIN 1

int main()
{
    stdio_init_all();

    // Initialize UART
    uart_init(UART_ID, BAUD_RATE);

    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);

    while (true) {

        // STM32 -> computer
        if (uart_is_readable(UART_ID))
        {
            char ch = uart_getc(UART_ID);
            printf("%c", ch);
            //putchar(ch);   
            stdio_flush();
        }

        // Computer -> STM32
        int c = getchar_timeout_us(0);

        if (c != PICO_ERROR_TIMEOUT)
        {
            uart_putc(UART_ID, (char)c);
        }
    }
}
