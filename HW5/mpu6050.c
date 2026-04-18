#include <string.h> // for memset
#include <stdint.h>

#include "mpu6050.h"

#include "hardware/i2c.h"
#include "pico/stdlib.h"

/*************************************************************
 Functions that initalize, check, and read the IMU
*************************************************************/
void init_mpu6050(void){    

    // 1. Turn on the MPU
    write_byte_I2C0(MPU6050_ADDR, PWR_MGMT_1, 0x00);

    // 2. Set accel. sensitivity to +-2g
    write_byte_I2C0(MPU6050_ADDR, ACCEL_CONFIG, 0x00);

    // 3. Set gyro +-2000 dps
    write_byte_I2C0(MPU6050_ADDR, GYRO_CONFIG, 0x18);

}

// Verifies the identity of the MPU 6050
uint8_t whoami(void){
    return read_byte_I2C0(MPU6050_ADDR, WHO_AM_I);
}

// Burst read from MPU_6050, from ACCEL_XOUT_H reg through GYRO_ZOUT_L reg
void burst_read_mpu6050(uint8_t * data){
    burst_read_I2C0(MPU6050_ADDR, ACCEL_XOUT_H, data, IMU_ARRAY_LEN);
}

/*************************************************************
 Functions that combine 8-bit register pairs (each uint8_t) into int16_t's:
*************************************************************/

// Convert x-acc. to int16_t
int16_t get_xXL(uint8_t * data){
    return data[0]<<8 | data[1];
}

// Convert y-acc. to int16_t
int16_t get_yXL(uint8_t * data){
    return data[2]<<8 | data[3];
}

// Convert z-acc. to int16_t
int16_t get_zXL(uint8_t * data){
    return data[4]<<8 | data[5];
}

// Convert temp. to int16_t
int16_t get_temp(uint8_t * data){
    return data[6]<<8 | data[7];
}

// Convert x-gyro to int16_t
int16_t get_xG(uint8_t * data){
    return data[8]<<8 | data[9];
}

// Convert y-gyro to int16_t
int16_t get_yG(uint8_t * data){
    return data[10]<<8 | data[11];
}

// Convert z-gyro to int16_t
int16_t get_zG(uint8_t * data){
    return data[12]<<8 | data[13];
}

/*************************************************************
 Functions that convert int16_t representation of 16-bit IMU data
 (acceleration in x, y, and z; temperature; gyro rates) to float representation
*************************************************************/

// Convert x-acc. to float (g's)
float conv_xXL(uint8_t * data){
    return (get_xXL(data)*0.000061);
}

// Convert y-acc. to float (g's)
float conv_yXL(uint8_t * data){
    return (get_yXL(data)*0.000061);
}

// Convert z-acc. to float (g's)
float conv_zXL(uint8_t * data){
    return (get_zXL(data)*0.000061);
}

// Convert x-gyro rate to dps
float conv_xG(uint8_t * data){
    return (get_xG(data)*0.007630);
}

// Convert y-gyro rate to dps
float conv_yG(uint8_t * data){
    return (get_yG(data)*0.007630);
}

// Convert z-gyro rate to dps
float conv_zG(uint8_t * data){
    return (get_zG(data)*0.007630);
}

// Convert int16_t temperature signed short to float (Celsius)
float conv_temp(uint8_t * data){
    return (get_temp(data)/340.00)+ 36.53;
}

/*************************************************************
 I2C Functions
*************************************************************/

// Read one byte from a register 
uint8_t read_byte_I2C0(uint8_t dev_addr, uint8_t reg_addr){
    uint8_t val;

    i2c_write_blocking(i2c_default, dev_addr, &reg_addr, 1, true);
    i2c_read_blocking(i2c_default, dev_addr, &val, 1, false);

    return val;
}

// burst read from device (dev_addr), beginning at specified register
// by start reg_addr:
uint8_t burst_read_I2C0(uint8_t dev_addr, uint8_t start_reg_addr, uint8_t * data, uint8_t data_len){

    // Tell IMU where to start reading
    i2c_write_blocking(i2c_default, dev_addr, &start_reg_addr, 1, true);

    // Read all bytes at once
    i2c_read_blocking(i2c_default, dev_addr, data, data_len, false);

    return 0;
}

// write one byte (data) from a register (reg addr) of a device (dev_addr):
void write_byte_I2C0(uint8_t dev_addr, uint8_t reg_addr, uint8_t data){
    uint8_t buf[2];
    buf[0] = reg_addr;
    buf[1] = data;

    i2c_write_blocking(i2c_default, dev_addr, buf, 2, false);
}
