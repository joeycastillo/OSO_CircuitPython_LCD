import board
import time
import rtc
from oso_lcd.lcdwing_lite import LCDWingLite, Indicator

display = LCDWingLite(board.I2C())
minute = None
clock = rtc.RTC()
clock.datetime = time.struct_time((2022, 6, 30, 11, 59, 55, 0, -1, -1))

while True:
    if minute != clock.datetime.tm_min:
        dt = clock.datetime
        hour = dt.tm_hour % 12
        minute = dt.tm_min
        display.clear_indicator(Indicator.ALL)
        display.print("{:2d}:{:02d}".format(hour if hour else 12, minute))
        if dt.tm_hour < 12:
            display.set_indicator(Indicator.AM)
        else:
            display.set_indicator(Indicator.PM)
    display.toggle_colon()
    time.sleep(0.5)
