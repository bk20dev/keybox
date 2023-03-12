from machine import Pin


class VirtualPin:
    def __init__(self, pin: int, reg, val=0):
        self._pin = pin
        self._reg = reg
        self._val = val

    # noinspection PyProtectedMember
    def value(self, val: int | None = None) -> int:
        if val is not None:
            self._val = val
            self._reg._shift_out()
        return self._val


class N74HC595:
    def __init__(self, ds: Pin, sck: Pin, rck: Pin, width: int = 8, val: int = 0):
        self._ds = ds
        self._sck = sck
        self._rck = rck
        self._width = width
        self._virtual_pins = [VirtualPin(pin, self, val=val) for pin in range(width)]
        self._shift_out()

    def _write(self, val: list[int]) -> None:
        self._rck.value(0)
        for x in reversed(val):
            self._ds.value(x)
            self._sck.value(0)
            self._sck.value(1)
        self._rck.value(1)

    def _shift_out(self) -> None:
        self._write(self._value)

    @property
    def _value(self) -> list[int]:
        return [pin.value() for pin in self._virtual_pins]

    def __len__(self) -> int:
        return len(self._virtual_pins)

    def __getitem__(self, pin: int) -> VirtualPin | None:
        assert 0 <= pin < self._width
        return self._virtual_pins[pin]
