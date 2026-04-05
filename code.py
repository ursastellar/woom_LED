import board
import digitalio
import neopixel
import time

# 1. Open the Power Gate (Essential for Prop-Maker)
power = digitalio.DigitalInOut(board.EXTERNAL_POWER)
power.direction = digitalio.Direction.OUTPUT
power.value = True

# 2. Setup the strip
# Note: Use EXTERNAL_NEOPIXELS for the green screw terminal
pixels = neopixel.NeoPixel(board.EXTERNAL_NEOPIXELS, 60, brightness=0.2, auto_write=True)


print("System Initialized: Woom-Glow is ONLINE")

while True:
    # 3. Solid Purple Glow
    pixels.fill((180, 0, 255)) 
    print("Status: Purple Glow Active")
    time.sleep(2)
    
    # 4. Heartbeat Pulse (To show it's working)
    pixels.fill((255, 255, 255)) # Flash White
    print("Status: Motion/Safety Pulse")
    time.sleep(0.1)
