# IoT Emergency Alert System (ESP32 & MicroPython)

An automated emergency distress system that leverages an ESP32 microcontroller and a companion mobile application to instantly broadcast SOS alerts, GPS locations, and timestamps to pre-configured emergency contacts over SMS.

---

## 📄 Project Overview

The **IoT Emergency Alert System** is a low-latency, hardware-to-mobile safety solution designed for vulnerable individuals, outdoor adventurers, or industrial workers. Built on the **ESP32** platform using **MicroPython**, this device serves as a physical panic button. 

When the physical trigger on the ESP32 is activated, it instantly broadcasts an encrypted or structured `"help"` distress payload via **Bluetooth Low Energy (BLE)** to a paired mobile application. Upon receiving this signal, the background service of the mobile application fetches the smartphone's real-time **GPS coordinates** and local **timestamp**, automatically dispatching an SMS distress message to a list of designated emergency contacts without requiring the user to open or unlock their phone.

---

## 🛠️ Hardware Requirements

To replicate or build this project, you will need the following hardware components:

* **ESP32 Development Board:** (e.g., ESP32-WROOM-32 NodeMCU) Chosen for its integrated dual-mode Bluetooth (Classic and BLE) and low power consumption states.
* **LED Display:** To display "MESSAGING CONTACTS" when user pressed the button
* **Physical Tactile Button / Push Button:** Acts as the hardware interrupt trigger for the emergency broadcast.
* **Breadboard & Jumper Wires:** For prototyping and establishing connections between the button and the microcontroller.
* **Micro-USB Cable:** For flashing the MicroPython firmware and uploading scripts to the ESP32.

---

## 📚 Libraries & Frameworks

The system relies on the following core libraries and software modules:

### MicroPython (Firmware Side)
* **`ubluetooth` / `bluetooth`:** Built-in MicroPython module used to interact with the ESP32's onboard BLE controller, handle advertising payloads, and manage the GATT server profiles.
* **`machine`:** Standard MicroPython module used to control hardware peripherals, configure GPIO pins for the tactile button, and handle hardware-level interrupts (`IRQ_RISING`).
* **`utime`:** Provides time-keeping and delay functions necessary for debouncing the physical switch and managing BLE advertising intervals.
