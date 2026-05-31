import time

class LcdApi:
    # LCD Comands
    LCD_CLR = 0x01
    LCD_HOME = 0x02
    LCD_ENTRY_MODE = 0x04
    LCD_DISPLAY_CONTROL = 0x08
    LCD_CURSOR_SHIFT = 0x10
    LCD_FUNCTION_SET = 0x20
    LCD_SET_CGRAM_ADDR = 0x40
    LCD_SET_DDRAM_ADDR = 0x80

    # Flags for display entry mode
    LCD_ENTRY_RIGHT = 0x00
    LCD_ENTRY_LEFT = 0x02
    LCD_ENTRY_SHIFT_INCREMENT = 0x01
    LCD_ENTRY_SHIFT_DECREMENT = 0x00

    # Flags for display on/off control
    LCD_DISPLAY_ON = 0x04
    LCD_DISPLAY_OFF = 0x00
    LCD_CURSOR_ON = 0x02
    LCD_CURSOR_OFF = 0x00
    LCD_BLINK_ON = 0x01
    LCD_BLINK_OFF = 0x00

    # Flags for display/cursor shift
    LCD_DISPLAY_MOVE = 0x08
    LCD_CURSOR_MOVE = 0x00
    LCD_MOVE_RIGHT = 0x04
    LCD_MOVE_LEFT = 0x00

    # Flags for function set
    LCD_8BIT_MODE = 0x10
    LCD_4BIT_MODE = 0x00
    LCD_2_LINE = 0x08
    LCD_1_LINE = 0x00
    LCD_5x10_DOTS = 0x04
    LCD_5x8_DOTS = 0x00

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        if self.num_lines > 4:
            self.num_lines = 4
        self.num_columns = num_columns
        if self.num_columns > 40:
            self.num_columns = 40
        self.cursor_x = 0
        self.cursor_y = 0
        self.implied_newline = False
        self.display_control = self.LCD_DISPLAY_ON | self.LCD_CURSOR_OFF | self.LCD_BLINK_OFF
        self.backlight = True

    def clear(self):
        self.hal_write_command(self.LCD_CLR)
        self.hal_write_command(self.LCD_HOME)
        self.cursor_x = 0
        self.cursor_y = 0

    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3f
        if cursor_y & 1:
            addr += 0x40
        if cursor_y & 2:
            addr += self.num_columns
        self.hal_write_command(self.LCD_SET_DDRAM_ADDR | addr)

    def putchar(self, char):
        if char == '\n':
            self.cursor_x = 0
            self.cursor_y += 1
            if self.cursor_y >= self.num_lines:
                self.cursor_y = 0
            self.move_to(self.cursor_x, self.cursor_y)
        else:
            self.hal_write_data(ord(char))
            self.cursor_x += 1
            if self.cursor_x >= self.num_columns:
                self.putchar('\n')

    def putstr(self, string):
        for char in string:
            self.putchar(char)
