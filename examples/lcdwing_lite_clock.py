import board
import time
import rtc
from oso_lcd.lcdwing_lite import LCDWingLite, Indicator

r = rtc.RTC()
display = LCDWingLite(board.I2C())

# TODO: Replace this with your local time.
r.datetime = time.struct_time((2022, 4, 19, 11, 59, 52, 0, -1, -1))
last_min = None

while True:
    if last_min != r.datetime.tm_min:
        dt = r.datetime
        hour = dt.tm_hour % 12
        display.print("{:2d}:{:02d}".format(hour if hour else 12, r.datetime.tm_min))
        last_min = r.datetime.tm_min
        if dt.tm_hour < 12:
            display.clear_indicator(Indicator.PM)
            display.set_indicator(Indicator.AM)
        else:
            display.clear_indicator(Indicator.AM)
            display.set_indicator(Indicator.PM)
    display.set_indicator(Indicator.COLON)
    time.sleep(0.5)
    display.clear_indicator(Indicator.COLON)
    time.sleep(0.5)
