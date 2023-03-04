from machine import Pin

from N74HC595 import N74HC595

builtin_led = Pin(25, Pin.OUT)
builtin_led.value(1)

data_output = Pin(6, Pin.OUT)  # ds (14)
data_clock = Pin(7, Pin.OUT)  # sh_cp (11)
register_latch = Pin(8, Pin.OUT)  # st_cp (12)

register = N74HC595(data_output, data_clock, register_latch, width=8)
register[1].value(1)
