import board
import pwmio
import digitalio
import time

# Define pins for Motor 1
PWM_PIN = board.GP18
DIR_PIN = board.GP1
BUTTON_PIN = board.GP16

# Setup PWM and direction pins for Motor 1
pwm = pwmio.PWMOut(PWM_PIN, frequency=1000, duty_cycle=0)
dir_pin = digitalio.DigitalInOut(DIR_PIN)
dir_pin.direction = digitalio.Direction.OUTPUT

# Setup button pin
button = digitalio.DigitalInOut(BUTTON_PIN)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Use internal pull-up resistor

# Function to set motor speed and direction
def set_motor_speed(pwm, dir_pin, speed):
    if speed < 0:
        dir_pin.value = False  # Set direction to reverse
        pwm.duty_cycle = -speed
    else:
        dir_pin.value = True  # Set direction to forward
        pwm.duty_cycle = speed

# Function to stop the motor
def stop_motor(pwm):
    pwm.duty_cycle = 0

# State variables
direction = 1  # 1 for clockwise, -1 for counter-clockwise
motor_running = False

# Main loop
print("Press and hold the button to turn the motor. Release to stop.")
while True:
    if not button.value:  # Button pressed
        if not motor_running:  # If motor is not already running
            set_motor_speed(pwm, dir_pin, 65535 * direction)
            motor_running = True
            print("Motor running in direction:", "clockwise" if direction == 1 else "counterclockwise")
    else:  # Button not pressed
        if motor_running:  # If motor is currently running
            stop_motor(pwm)
            motor_running = False
            direction *= -1  # Toggle direction for next press
            print("Motor stopped. Next direction:", "clockwise" if direction == 1 else "counterclockwise")

    time.sleep(0.01)  # Small delay to debounce the button
