#ifndef MPU6050_H__
#define MPU6050_H__

#include <stdint.h>

#define MPU6050_ADDR 0x68
#define IMU_ARRAY_LEN 14  // 14 contiguous registers from ACCEL_XOUT to GYRO_ZOUT_L

// config registers
#define CONFIG 0x1A
#define GYRO_CONFIG 0x1B
#define ACCEL_CONFIG 0x1C
#define PWR_MGMT_1 0x6B
#define PWR_MGMT_2 0x6C

// sensor data registers
#define ACCEL_XOUT_H 0x3B
#define ACCEL_XOUT_L 0x3C
#define ACCEL_YOUT_H 0x3D
#define ACCEL_YOUT_L 0x3E
#define ACCEL_ZOUT_H 0x3F
#define ACCEL_ZOUT_L 0x40
#define TEMP_OUT_H   0x41
#define TEMP_OUT_L   0x42
#define GYRO_XOUT_H  0x43
#define GYRO_XOUT_L  0x44
#define GYRO_YOUT_H  0x45
#define GYRO_YOUT_L  0x46
#define GYRO_ZOUT_H  0x47
#define GYRO_ZOUT_L  0x48
#define WHO_AM_I     0x75


// All functions
void init_mpu6050(void);
uint8_t whoami(void);

void burst_read_mpu6050(uint8_t * data);

int16_t get_xXL(uint8_t * data);
int16_t get_yXL(uint8_t * data);
int16_t get_zXL(uint8_t * data);
int16_t get_temp(uint8_t * data);
int16_t get_xG(uint8_t * data);
int16_t get_yG(uint8_t * data);
int16_t get_zG(uint8_t * data);

float conv_xXL(uint8_t * data);
float conv_yXL(uint8_t * data);
float conv_zXL(uint8_t * data);
float conv_xG(uint8_t * data);
float conv_yG(uint8_t * data);
float conv_zG(uint8_t * data);
float conv_temp(uint8_t * data);

// i2c functions

// read one byte from a register (reg_addr) of a device (dev_addr) :
uint8_t read_byte_I2C0(uint8_t dev_addr,
                       uint8_t reg_addr);

// burst read from device (dev_addr), beginning at specified register
// by start reg_addr:
uint8_t burst_read_I2C0(uint8_t dev_addr,
                       uint8_t start_reg_addr,
                       uint8_t * data,
                       uint8_t data_len);

// write one byte (data) from a register (reg addr) of a device (dev_addr):
void write_byte_I2C0(uint8_t dev_addr,
                     uint8_t reg_addr,
                     uint8_t data);

#endif