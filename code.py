import time
import board
import digitalio
import neopixel
import adafruit_lis3dh
import math

# 1. Power Gate
power = digitalio.DigitalInOut(board.EXTERNAL_POWER)
power.direction = digitalio.Direction.OUTPUT
power.value = True

# 2. LED Setup (60 LEDs)
pixels = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, 60, brightness=0.5, auto_write=False)

# 3. Sensor Setup
i2c = board.I2C()
accel = adafruit_lis3dh.LIS3DH_I2C(i2c)

# --- SETTINGS ---
PURPLE = (180, 0, 255)
BRAKE_RED = (255, 0, 0)
BRAKE_THRESHOLD = 20.0  # Sharp impact
MOVE_THRESHOLD = 4.0     # Sensitivity to wiggles (lower = more sensitive)
IDLE_TIMEOUT = 10.0      # Seconds until power-off

# Variables for Delta Math
last_x, last_y, last_z = accel.acceleration
last_move_time = time.monotonic()
pulse_index = 0.0

print("--- Woom-Glow: Delta-Motion System ONLINE ---")

while True:
    now = time.monotonic()
    x, y, z = accel.acceleration
    
    # --- DELTA MATH (The Secret Sauce) ---
    # We calculate how much the acceleration CHANGED since the last loop
    # This ignores gravity because gravity is constant!
    dx = abs(x - last_x)
    dy = abs(y - last_y)
    dz = abs(z - last_z)
    vibration = dx + dy + dz
    
    # Save current values for the next loop
    last_x, last_y, last_z = x, y, z

    # 1. BRAKE CHECK (High Priority)
    if vibration > BRAKE_THRESHOLD:
        print(f"BRAKE! Delta: {vibration:.2f}")
        pixels.fill(BRAKE_RED)
        pixels.show()
        last_move_time = now
        time.sleep(0.4)
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.05)

    # 2. MOVEMENT CHECK
    elif vibration > MOVE_THRESHOLD:
        # Bike is moving or being touched
        last_move_time = now
        pulse_index += 0.05
        breath = (math.sin(pulse_index) + 1) / 4 + 0.1
        pixels.fill((int(PURPLE[0]*breath), int(PURPLE[1]*breath), int(PURPLE[2]*breath)))
        pixels.show()
        print(f"MOVING - Delta: {vibration:.2f} | Time Left: {IDLE_TIMEOUT:.1f}")

    # 3. IDLE / PARKED CHECK
    else:
        time_elapsed = now - last_move_time
        if time_elapsed > IDLE_TIMEOUT:
            # Fully Parked - Turn off
            pixels.fill((0, 0, 0))
            pixels.show()
        else:
            # Cooling down - Slow Purple
            pulse_index += 0.02
            breath = (math.sin(pulse_index) + 1) / 6 + 0.05
            pixels.fill((int(PURPLE[0]*breath), int(PURPLE[1]*breath), int(PURPLE[2]*breath)))
            pixels.show()
            # print(f"IDLE - Delta: {vibration:.2f} | Time Left: {IDLE_TIMEOUT - time_elapsed:.1f}")

    time.sleep(0.05) # Slightly slower loop for better delta stability
