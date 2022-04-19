# SPDX-FileCopyrightText: Joey Castillo 2022 for Oddly Specific Objects
#
# SPDX-License-Identifier: MIT

"""
`oso_lcd.bu9796_lite`
===========================
* Authors: Joey Castillo
* Based on adafruit_ht16k33 by Radomir Dopieralski & Tony DiCola for Adafruit Industries
"""

from adafruit_bus_device import i2c_device
from micropython import const
from busio import I2C

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/joeycastillo/OSO_CircuitPython_LCD.git"

class BU9796Lite:
    """
    Lightweight BU9796 driver for space-constrained devices. No blink function!
    :param I2C i2c: The I2C bus object
    :param int address: The I2C addess of the BU9796.
    :param bool auto_write: True if the display should immediately change when
        set. If False, `show` must be called explicitly.
    """

    def __init__(
        self,
        i2c: I2C,
        address: int = 0x3e,
        auto_write: bool = True
    ) -> None:
        self.i2c_device = i2c_device.I2CDevice(i2c, address)
        self._cmd = bytearray(1)
        self._temp = bytearray(6)
        self._buffer = bytearray(7)
        self._auto_write = auto_write
        self.fill(0)
        self._write_cmd(0b00111100) # Configure for lowest power consumption
        self._write_cmd(0b01001000) # display ON, 1/3 bias

    def _write_cmd(self, byte: bytearray) -> None:
        self._cmd[0] = byte
        with self.i2c_device:
            self.i2c_device.write(self._cmd)

    @property
    def auto_write(self) -> bool:
        """Auto write updates to the display."""
        return self._auto_write

    @auto_write.setter
    def auto_write(self, auto_write: bool) -> None:
        self._auto_write = auto_write

    def show(self) -> None:
        """Refresh the display and show the changes."""
        with self.i2c_device:
            self.i2c_device.write(self._buffer)

    def show_partial(self, length: int = 1, *, pos = 0) -> None:
        """Transmit only some of the buffer."""
        with self.i2c_device:
            if pos:
                self._temp[0] = pos * 2
                self._temp[1:1+length] = self._buffer[pos+1:pos+length+1]
                self.i2c_device.write(self._temp[0:1+length])
            else:
                self.i2c_device.write(self._buffer[:1+length])

    def fill(self, on: bool) -> None:
        """Turn all pixels on or off
        :param bool on: Desired state for all pixels
        """
        fill = 0xFF if on else 0x00
        for i in range(1, len(self._buffer)):
            self._buffer[i] = fill
        if self._auto_write:
            self.show()

    def _set_buffer(self, i: int, value: bool) -> None:
        self._buffer[i + 1] = value # Offset by 1 to move past address byte.

    def _get_buffer(self, i: int) -> bool:
        return self._buffer[i + 1]  # Offset by 1 to move past address byte.
