from machine import Pin, SoftI2C
import time
from esp32_i2c_lcd import I2cLcd

#prepare button for trigger
#when the user pressed the button, send a message to pluetooth paired device
button = Pin(4,Pin.IN,Pin.PULL_UP)


# 1. Define ESP32 I2C pins (SDA=GPIO 21, SCL=GPIO 22)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)


#0X27 0x3F
I2C_ADDR = 0x27
total_rows = 2
total_cols = 16

#Initialize the LCD
lcd = I2cLcd(i2c, I2C_ADDR, total_rows, total_cols)

# Clear the screen
lcd.clear()


while True:
    
    if button.value() == 0:
        #display message to the screen "SENDING HELP TO CONTACTS"
        lcd.move_to(0,0)
        lcd.putstr("MESSAGING")
        lcd.move_to(0,1)
        lcd.putstr("CONTACTS")
        
    
    #little rest for the chip
    time.sleep(0.03)
        