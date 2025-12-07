# WoW RGB Health Monitor (Scanner Bar Edition) ⚔️📠
![Diagrama](resources/icon.ico)
> **Why? Because I can.**

An immersive ambient lighting system for **Turtle WoW** (1.12.1) born from recycling, but engineered to be universal. This project converts your in-game health status into real-time room lighting (Green > Yellow > Red), powered by an ESP8266.

While this prototype was built scavenging the **CIS (Contact Image Sensor)** light bar from a broken printer/scanner, **the firmware and software are fully compatible with any standard 5V Analog RGB LED strip.**

![Status](https://img.shields.io/badge/Status-Stable-green) ![Hardware](https://img.shields.io/badge/Hardware-Universal-orange) ![License](https://img.shields.io/badge/License-MIT-blue)

## 🤯 The Concept

The idea started as a challenge: could I save a scanner light bar from the landfill and turn it into a gaming peripheral?
The result is a standalone device that reacts to your character's life:
* **100% HP:** Bright Green.
* **50% HP:** Warning Yellow.
* **<10% HP:** Critical Red.

## ✨ Software Features

* **Plug & Play:** Portable `.exe` application. No Python installation or library setup required.
* **Universal Hardware:** Works with recycled scanner bars OR standard commercial 5050 RGB analog strips.
* **WiFi Manager:** The ESP creates its own Hotspot for initial setup. No hardcoded WiFi credentials!
* **Zero-Lag:** Optimized network protocol using persistent HTTP sessions and local DNS resolution (`wowrgb.local`).
* **Stealth Mode:** Minimizes to the System Tray (near the clock). No annoying console windows.
* **Manual Control:** Right-click menu to use the lamp as a static mood light (Fixed Colors) when you are not gaming.

## 🛠️ Hardware Requirements

The system is designed to be powered via **USB (5V)**.

1.  **Microcontroller:** ESP-01 or ESP-01S (ESP8266).
2.  **Voltage Regulator:** **LM3940** (5V to 3.3V LDO).
    * *Alternative:* AMS1117-3.3 module.
3.  **Capacitors (For LM3940 stability):**
    * 1x **47µF Ceramic** (Input side).
    * 1x **33µF Electrolytic** (Output side).
4.  **Lights (Choose one):**
    * **Option A (The Scavenger):** Recycled Printer/Scanner LED Bar (CIS Module). *Must be 5V.*
    * **Option B (The Standard):** Any generic 5V Analog RGB LED strip (Common Anode).
5.  **Drivers:** 2x NPN Transistors (BC547, 2N2222, or similar).
6.  **Resistors:** 2x 1kΩ (for Transistor Bases).
7.  **Power:** PC USB Port or Phone Charger.

### Wiring Diagram (Split Voltage)
* **USB 5V (+):** Goes to **LED Strip Anode**, **Regulator Input**, and **47µF Capacitor (+)**.
* **Regulator Output (3.3V):** Goes to **ESP-01 VCC & CH_PD** and **33µF Capacitor (+)**.
* **Red Channel (-):** To Transistor 1 Collector -> Base to **GPIO 0**.
* **Green Channel (-):** To Transistor 2 Collector -> Base to **GPIO 2**.
* **GND:** Common Ground for ALL components (USB, ESP, Emitters, and Capacitors negative).

*(Note: This project uses only 2 channels (Red/Green) to mix Yellow. The Blue channel is left disconnected for this specific Health Bar effect).*

## 📦 Installation & Usage

### 1. Game Setup (Addon)
Copy the `WoW_RGB` folder into your game directory:
`.../Interface/AddOns/`
* *This creates an invisible reference frame that the software reads.*

### 2. Hardware Setup
Plug your USB device in.
Only for the first time:
* Search for the WiFi network `WoWRGB` on your phone or pc.
* Connect and configure it with your home WiFi credentials.
* The device will reboot and is ready to go.

### 3. Software Launch
1.  Open **WoW**.
2.  **Requirement:** Set Video Options to **"Windowed Fullscreen"** or **"Fullscreen"**.
3.  Run `WoW_RGB_Control.exe`.
4.  You will see the icon in your system tray. Ready to play!

## ⚙️ Controls
**Right-Click** the system tray icon to access the menu:
* **WoW Mode (Auto):** Syncs lighting with game health.
* **Fixed [Red/Green/Yellow]:** Sets static ambient lighting.
* **Turn Off:** Turns off LEDs without closing the app.
* **Exit:** Closes the app.

---

### ⚠️ Disclaimer
This project is **Output-Only**. It utilizes passive screen capture (1x1 pixel) to read the game state. **It does not inject code into memory, does not send keystrokes, and does not automate actions (botting).** It complies with the non-interference policy of the Turtle WoW client, acting solely as a visual indicator (Ambilight style).

**Made with code, solder, and things other people threw away.** ♻️

