# SPDX-FileCopyrightText: Joey Castillo 2022 for Oddly Specific Objects
#
# SPDX-License-Identifier: MIT

"""
`oso_lcd.lcdwing_lite`
===========================
* Authors: Joey Castillo
* Based on adafruit_ht16k33 by Radomir Dopieralski & Tony DiCola for Adafruit Industries
"""

from oso_lcd.bu9796_lite import BU9796Lite

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/joeycastillo/OSO_CircuitPython_LCD.git"

CHARS = (
    0b00000000, # [space]
    0b00101100, # !
    0b01001000, # "
    0b11001010, # # (°)
    0b00000000, # $ (TODO)
    0b00000000, # % (TODO)
    0b00000000, # & (TODO)
    0b00000000, # ' (TODO)
    0b00000000, # ( (TODO)
    0b00000000, # ) (TODO)
    0b00000000, # * (TODO)
    0b00000000, # + (TODO)
    0b00000000, # , (TODO)
    0b00000010, # -
    0b00100000, # .
    0b00001100, # /
    0b11011101, # 0
    0b00001100, # 1
    0b10011011, # 2
    0b10001111, # 3
    0b01001110, # 4
    0b11000111, # 5
    0b11010111, # 6
    0b10001100, # 7
    0b11011111, # 8
    0b11001111, # 9
    0b00000000, # : (TODO)
    0b00000000, # ; (TODO)
    0b00000000, # < (TODO)
    0b00000000, # = (TODO)
    0b00000000, # > (TODO)
    0b10011010, # ?
    0b11111111, # @
    0b11011110, # A
    0b01010111, # B
    0b11010001, # C
    0b00011111, # D
    0b11010011, # E
    0b11010010, # F
    0b11001111, # G
    0b01010110, # H
    0b00010000, # I
    0b00001101, # J
    0b11010110, # K
    0b01010001, # L
    0b11011100, # M
    0b00010110, # N
    0b00010111, # O
    0b11011010, # P
    0b11001110, # Q
    0b00010010, # R
    0b11000101, # S
    0b01010011, # T
    0b01011101, # U
    0b00011101, # V
    0b01011111, # W
    0b01011110, # X
    0b01001111, # Y
    0b10011001, # Z
)

class Indicator:
    AM = const(0b10000000)
    PM = const(0b01000000)
    BATTERY = const(0b00100000)
    BELL = const(0b00001000)
    WIFI = const(0b00000100)
    DATA = const(0b00000010)
    MOON = const(0b00000001)
    ALL = const(0b11101111)

class LCDWingLite(BU9796Lite):
    """
    Lightweight driver for LCD FeatherWing. Only supports printing strings.
        Note that for show_partial calls with this display glass, position
        0 represents the indicator icons. Postions 1-5 are the digits.
    """
    def print(self, value: str) -> None:
        """Prints a string to the display."""
        value = value.upper()
        neg = value[0] == '-'
        pos = 1 if neg else 0
        d = False
        i = 1
        self._set_buffer(0, self._get_buffer(0) & ~0b00010000)
        while i < 6:
            b = 0
            try:
                c = value[pos]
                pos += 1
                if c == '.':
                    d = True
                    continue
                elif c == ':':
                    if i == 3:
                        self._set_buffer(0, self._get_buffer(0) | 0b00010000)
                    continue
                b = CHARS[ord(c) - 32]
            except:
                b = 0b00100000 if d else 0
            self._set_buffer(i, b | (0b00100000 if (neg and i == 1) or d else 0))
            i += 1
            d = False
        if self.auto_write:
            self.show()

    def set_indicator(self, indicator: byte):
        """Sets one of the indicators. Values are in lcdwing_lite.Indicators"""
        self._set_buffer(0, self._get_buffer(0) | indicator)
        if self._auto_write:
            self.show_partial(1)

    def clear_indicator(self, indicator: int):
        """Clears one of the indicators."""
        self._set_buffer(0, self._get_buffer(0) & ~indicator)
        if self._auto_write:
            self.show_partial(1)
