from machine import Pin, SPI

from mfrc522 import MFRC522
from n74hc595 import N74HC595

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

register = N74HC595(data_output, data_clock, register_latch, width=8)
# reader = MFRC522(spi, sda, lambda pin: register[pin], width=8)

reader = MFRC522(spi, sda, register[0])

while True:
    led.value(1)
    reader.init()
    (status, tag_type) = reader.request(MFRC522.REQIDL)
    led.value(0)

    if status == MFRC522.OK:
        (status, uid) = reader.anticoll(MFRC522.PICC_ANTICOLL1)
        if status == MFRC522.OK:
            led_read_ok.value(1)
            print(f"ok, {uid}")
        else:
            led_read_ok.value(0)
            print("err: select_tag_sn")
    else:
        led_read_ok.value(0)
        print("err: request")
