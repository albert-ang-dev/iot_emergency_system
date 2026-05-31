from machine import Pin, SoftI2C
import time
from ble_uart import ESP32BLE
from esp32_i2c_lcd import I2cLcd

# Prepare button for trigger
button = Pin(4, Pin.IN, Pin.PULL_UP)

# Define ESP32 I2C pins
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)

I2C_ADDR = 0x27
total_rows = 2
total_cols = 16

# Initialize the LCD
lcd = I2cLcd(i2c, I2C_ADDR, total_rows, total_cols)
lcd.clear()

# State Variables to prevent constant screen flickering
appResponded = False
last_connected_state = False

def on_data_received(incoming_string):
    global appResponded
    
    if incoming_string.lower() == "sent":
        appResponded = True

ble_device = ESP32BLE(name="ESP32_Serial")
ble_device.on_receive(on_data_received)

print("Bluetooth is active. Connect via app.")
lcd.putstr("CONNECT TO APP")

while True:
    current_connected_state = ble_device.is_connected()
    
    if current_connected_state:
        if not last_connected_state:
            lcd.clear()
            lcd.putstr("CONNECTED SUCCESS!")
            last_connected_state = True
        
        #The phone sent the "sent" message
        if appResponded:
            lcd.clear()
            lcd.putstr("DONE")
            time.sleep(5)      # Safe to sleep here in the main loop
            lcd.clear()
            lcd.putstr("CONNECTED SUCCESS!")
            appResponded = False # Reset the flag
        
        #Physical Button Press
        if button.value() == 0:
            lcd.clear()
            lcd.putstr("SENDING SOS")
            ble_device.send("Hi there from ESP32!")
            time.sleep(3)
            lcd.clear()
            lcd.putstr("CONNECTED SUCCESS!")
            
    else:
        # If the device disconnects, update the screen once
        if last_connected_state:
            lcd.clear()
            lcd.putstr("CONNECT TO APP")
            last_connected_state = False
            
    # Little rest for the chip
    time.sleep(0.05)
