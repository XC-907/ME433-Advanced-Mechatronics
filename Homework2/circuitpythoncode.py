# RC Servo sweep angle implementation (CircuitPython)
import board     # get pin definitions
import pwmio     # get PWM
import time      # get sleep function

# Create PWM Signal output on pin GP16
servo = pwmio.PWMOut(board.GP16, variable_frequency=True)

# Set Servo frequency
servo.frequency = 50 # hz

# Define minimum and maximum duty cycle
min_duty = int(65535*(0.4/20))    # 2% duty cycle
max_duty = int(65535*(2.4/20))    # 12% duty cycle

# Define set servo function
def set_servo_angle(angle):
    duty = int(min_duty + (max_duty-min_duty)*(angle/180))
    servo.duty_cycle = duty

while True:
    # Sweep forward (0 → 180)
    for angle in range(0, 181, 1):
        set_servo_angle(angle)
        time.sleep(0.01)
    
    # Sweep backward (180 → 0)
    for angle in range(181, 0, -1):
        set_servo_angle(angle)
        time.sleep(0.01)
