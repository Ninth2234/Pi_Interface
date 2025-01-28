from machine import Pin, PWM
import time

# Set up PWM on GPIO16
servo_pin = PWM(Pin(16))  # GP16
servo_pin.freq(50)        # Set frequency to 50 Hz for servos

def set_servo_angle(pin, angle):
    """
    Set the servo angle.
    
    Parameters:
    - pin: The PWM pin object.
    - angle: Desired angle (0 to 180 degrees).
    """
    # Convert angle to duty cycle (assuming 0.5ms to 2.5ms pulse width for 0° to 180°)
    min_duty = 1000  # Corresponds to 0.5ms pulse
    max_duty = 9000  # Corresponds to 2.5ms pulse
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    pin.duty_u16(duty)

try:
    while True:
        # Sweep servo from 0 to 180 degrees
        for angle in range(0, 181, 10):
            set_servo_angle(servo_pin, angle)
            time.sleep(0.05)
        
        # Sweep servo back from 180 to 0 degrees
        for angle in range(180, -1, -10):
            set_servo_angle(servo_pin, angle)
            time.sleep(0.05)
finally:
    # Cleanup
    servo_pin.deinit()
