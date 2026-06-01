# IoT Emergency Alert System (ESP32 & MicroPython)

An event-driven IoT distress system featuring an ESP32 microcontroller that pairs with a mobile application to instantly transmit emergency alerts upon a physical button press.

---

## 📄 Project Overview

The **IoT Emergency Alert System** is a low-latency, hardware-to-mobile communication solution built on the **ESP32** platform using **MicroPython**. Designed with a strict Finite State Machine (FSM), the device enforces a secure initialization workflow before enabling safety utility. 

### System Workflow
1. **Power-On & Pairing State:** Upon boot, the ESP32 blocks primary utility and prompts the user via an LED display to connect a mobile device.
2. **Ready State:** Once a successful **Bluetooth Low Energy (BLE)** handshake is confirmed with the mobile application, the device transitions to an active monitoring state.
3. **Alert State:** When the physical tactile button is pressed, the ESP32 instantly transmits a `"help"` payload to the paired mobile app while dynamically updating the LED display to show `"MESSAGING CONTACTS"`.

---

## 🛠️ Hardware Requirements

* **ESP32 Development Board:** (e.g., ESP32-WROOM-32) Utilized for its integrated BLE stack and low-power capabilities.
* **LED Display:** (e.g., I2C OLED or LCD screen) Used to guide the user through the pairing sequence and display `"MESSAGING CONTACTS"` during alert execution.
* **Physical Tactile Button:** Configured as an asynchronous hardware interrupt trigger for the emergency transmission.
* **Breadboard & Jumper Wires:** For prototyping connections between peripherals and GPIO pins.
* **Micro-USB Cable:** For flashing MicroPython firmware and script deployment.

---

## 📚 Libraries & Frameworks

### MicroPython (Firmware Side)
* **`ubluetooth`:** Built-in module used to configure the ESP32's onboard BLE controller, handle advertising payloads, and manage the GATT server profiles for mobile app pairing.
* **`machine`:** Used to control hardware peripherals, handle communication for the LED display, and manage hardware-level interrupts (`IRQ_RISING`) for the button.
* **`utime`:** Provides time-keeping functions required for software switch debouncing and BLE transmission intervals.

---

## ⚙️ Architecture & Implementation Details

### 1. Finite State Machine (FSM)
The firmware is structured around a strict state machine to guarantee predictable behavior and prevent false triggers before a connection is secured:
* **`STATE_INIT`**: Configures GPIOs, registers interrupts, and initializes the LED screen.
* **`STATE_PAIRING`**: Displays a prompt on the screen requiring a connection. The ESP32 enters BLE advertising mode.
* **`STATE_READY`**: Triggered via a BLE connection callback. The device activates the main control loop.
* **`STATE_ALERT`**: Triggered via a hardware interrupt. It immediately transmits the `"help"` string and updates the display.

### 2. Low-Latency Edge Triggering
To ensure maximum responsiveness during an emergency, the physical button does not rely on a standard polling loop. Instead, it utilizes a hardware-level **Interrupt Service Routine (ISR)** coupled with digital software debouncing to eliminate mechanical noise and transmit the alert payload instantly.
