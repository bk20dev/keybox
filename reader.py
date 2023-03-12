from machine import SPI, Pin

from mfrc522 import MFRC522


class Reader:
    def __init__(self, spi: SPI, sda: Pin, enable_pin, width: int):
        self._spi = spi
        self._sda = sda
        self._enable_pin = enable_pin
        self._mfrc = MFRC522(spi, sda, enable_pin(0))
        self._width = width

    def _read_card(self, enable_pin: Pin) -> list[int] | None:
        enable_pin.value(1)
        self._mfrc.init()
        card_uid = self._get_card_id()
        enable_pin.value(0)
        return card_uid

    def _get_card_id(self) -> list[int] | None:
        (status, tag_type) = self._mfrc.request(MFRC522.REQIDL)
        if status == MFRC522.OK:
            (status, card_id) = self._mfrc.anticoll(MFRC522.PICC_ANTICOLL1)
            if status == MFRC522.OK:
                return card_id
        return None

    def __len__(self) -> int:
        return self._width

    def __getitem__(self, reader_id: int) -> list[int] | None:
        assert 0 <= reader_id < self._width
        enable_pin = self._enable_pin(reader_id)
        if enable_pin is None:
            return None
        card_id = self._read_card(enable_pin)
        return card_id
