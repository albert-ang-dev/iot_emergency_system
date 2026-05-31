'''
    AI GENERATE API CODE FOR LCD DISPLAY
'''

import time
from machine import I2C
from lcd_api import LcdApi

# Mask values for configuring the DB4-DB7 pins of the LCD via the PCF8574
MASK_RS = 0x01
MASK_RW = 0x02
MASK_E  = 0x04
MASK_LIGHT = 0x08

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.i2c.writeto(self.i2c_addr, bytes([0]))
        time.sleep_ms(20)
        self.hal_write_init_nibble(0x30)
        time.sleep_ms(5)
        self.hal_write_init_nibble(0x30)
        time.sleep_ms(1)
        self.hal_write_init_nibble(0x30)
        self.hal_write_init_nibble(0x20)
        super().__init__(num_lines, num_columns)
        cmd = self.LCD_FUNCTION_SET | self.LCD_4BIT_MODE | self.LCD_2_LINE | self.LCD_5x8_DOTS
        self.hal_write_command(cmd)
        cmd = self.LCD_DISPLAY_CONTROL | self.LCD_DISPLAY_ON
        self.hal_write_command(cmd)
        self.clear()
        cmd = self.LCD_ENTRY_MODE | self.LCD_ENTRY_LEFT
        self.hal_write_command(cmd)

    def hal_write_init_nibble(self, nibble):
        byte = nibble & 0xf0
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_E | MASK_LIGHT]))
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_LIGHT]))

    def hal_write_command(self, cmd):
        byte = (cmd & 0xf0)
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_E | MASK_LIGHT]))
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_LIGHT]))
        byte = ((cmd << 4) & 0xf0)
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_E | MASK_LIGHT]))
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_LIGHT]))
        if cmd <= 3:
            time.sleep_ms(5)

    def hal_write_data(self, data):
        byte = (data & 0xf0)
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_RS | MASK_E | MASK_LIGHT]))
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_RS | MASK_LIGHT]))
        byte = ((data << 4) & 0xf0)
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_RS | MASK_E | MASK_LIGHT]))
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_RS | MASK_LIGHT]))
