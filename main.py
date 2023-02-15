from machine import Pin

builtin_led = Pin(25, Pin.OUT)
builtin_led.value(1)
