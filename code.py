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
NUM_LEDS = 60
pixels = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, NUM_LEDS, brightness=1.0, auto_write=False)

# 3. Sensor Setup
i2c = board.I2C()
accel = adafruit_lis3dh.LIS3DH_I2C(i2c)

# --- COLORS ---
COLOR_START = (180, 0, 255)  # Start of strip: Deep Purple
COLOR_END   = (0, 255, 255)  # End of strip: Electric Cyan
BRAKE_RED   = (255, 0, 0)

# Settings
last_x, last_y, last_z = accel.acceleration
last_move_time = time.monotonic()
pulse_index = 0.0

print("--- Woom-Glow: Gradient Verified ---")

while True:
    now = time.monotonic()
    x, y, z = accel.acceleration
    
    # Delta Math
    vibration = abs(x - last_x) + abs(y - last_y) + abs(z - last_z)
    last_x, last_y, last_z = x, y, z

    # 1. BRAKE CHECK
    if vibration > 22.0:
        pixels.fill(BRAKE_RED)
        pixels.show()
        last_move_time = now
        time.sleep(0.4)
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.05)

    # 2. MOVING STATE (Professional Bounce / Ping-Pong)
    elif vibration > 4.0:
        last_move_time = now
        
        # INCREASE for faster bounce (0.05 is a smooth sweep)
        BOUNCE_SPEED = 0.36
        pulse_index += BOUNCE_SPEED 
        
        # Triangle Wave math: converts pulse_index into a position (0 to 59)
        # This creates the "Ping-Pong" back and forth motion
        ping_pong = (math.asin(math.sin(pulse_index)) / (math.pi / 2) + 1) / 2
        leader_pixel = ping_pong * (NUM_LEDS - 1)
        
        for i in range(NUM_LEDS):
            # Calculate distance from the "leader" to create a soft glow
            dist = abs(i - leader_pixel)
            
            # If the pixel is close to the leader, make it bright
            # Adjust '5.0' to make the "bounce" wider or narrower
            if dist < 8.0:
                falloff = 1.0 - (dist / 8.0)
                # Saturated Deep Purple (no green!)
                r = int(180 * falloff)
                g = 0 
                b = int(255 * falloff)
            else:
                # Dim background purple so the bike isn't dark
                r, g, b = (20, 0, 40)
            
            pixels[i] = (r, g, b)
        
        pixels.show()

    # 3. PARKED CHECK
    else:
        if now - last_move_time > 10.0:
            pixels.fill((0, 0, 0))
            pixels.show()

    time.sleep(0.02)
