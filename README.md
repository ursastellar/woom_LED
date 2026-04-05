# Woom-Glow 4: Motion-Reactive Underglow

A CircuitPython project for a Woom 4 children's bike featuring motion-reactive purple LEDs. 
Built with an Adafruit RP2040 Prop-Maker Feather.

## 🛠 Hardware Components
* **Controller:** Adafruit RP2040 Prop-Maker Feather
* **LEDs:** BTF-LIGHTING WS2812B RGB Strip (IP65)
* **Power:** 4xAA Battery Pack (via JST-PH port)
* **Connectors:** 3-pin JST-SM Pigtails

## 🔌 Wiring Map (Screw Terminals)
| Pigtail Color | Function | Feather Terminal | Strip Pad |
| :--- | :--- | :--- | :--- |
| **Red** | +5V Power | **5V** | +5V |
| **White** | Ground (GND) | **G** | GND |
| **Green** | Data Signal | **Neo** | Din |

## 🚀 Setup Instructions
1. Install [CircuitPython 9.x](https://circuitpython.org/board/adafruit_feather_rp2040_prop_maker/) on the Feather.
2. Copy the contents of `/src` to the `CIRCUITPY` drive as `code.py`.
3. Ensure the following libraries are in the `/lib` folder:
   * `neopixel.mpy`
   * `adafruit_pixelbuf.mpy`
   * `adafruit_lis3dh.mpy` (for motion sensing)

## 🚲 Installation Tips
* **Resale Protection:** Use clear silicone tape on the Woom 4 frame before applying LED adhesive.
* **Vibration Resistance:** Apply a small dab of hot glue to the screw terminals once wires are tightened.
* **Weatherproofing:** Mount the Feather inside a top-tube bag with a "drip loop" for the wire entry.
