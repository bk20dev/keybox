from machine import Pin, SPI

from n74hc595 import N74HC595
from reader import Reader

builtin_led = Pin(25, Pin.OUT)
builtin_led.value(1)

data_output = Pin(6, Pin.OUT)  # ds (14)
data_clock = Pin(7, Pin.OUT)  # sh_cp (11)
register_latch = Pin(8, Pin.OUT)  # st_cp (12)

sck = Pin(2, Pin.OUT)
mosi = Pin(3, Pin.OUT)
miso = Pin(4)
sda = Pin(5, Pin.OUT)

led = Pin(25, Pin.OUT)
led_read_ok = Pin(16, Pin.OUT)

spi = SPI(0, baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

register = N74HC595(data_output, data_clock, register_latch, width=8, val=0)
reader = Reader(spi, sda, enable_pin=lambda pin: register[pin], width=2)

i = 0
while True:
    card_id = reader[i]
    if card_id is not None:
        led_read_ok.value(1)
        print(f"ok:\t{card_id}")
    else:
        led_read_ok.value(0)
        print("err:")
    i += 1
    if i >= len(reader):
        i = 0
