import board
import busio
import analogio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import MatrixScanner, KeysScanner
from kmk.modules import Module

from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306


class AnalogEncoder(Module):
    def __init__(self, pin, thresholds, cw, ccw):
        self.pin = pin
        self.thresholds = thresholds
        self.cw = cw
        self.ccw = ccw
        self.ain = None
        self.last = None

    def during_bootup(self, keyboard):
        self.ain = analogio.AnalogIn(self.pin)

    def before_matrix_scan(self, keyboard):
        val = self.ain.value
        state = self.get_state(val)

        if self.last is not None and state != self.last:
            if self.last == 3:
                if state == 2:
                    keyboard.tap_key(self.ccw)
                elif state == 1:
                    keyboard.tap_key(self.cw)

        self.last = state
        return keyboard

    def get_state(self, v):
        for i, t in enumerate(self.thresholds):
            if v < t:
                return i
        return len(self.thresholds)

    def after_matrix_scan(self, keyboard): return keyboard
    def before_hid_send(self, keyboard): return
    def after_hid_send(self, keyboard): return
    def on_powersave_enable(self, keyboard): return
    def on_powersave_disable(self, keyboard): return


keyboard = KMKKeyboard()

keyboard.matrix = [
    MatrixScanner(
        column_pins=(board.D1, board.D2, board.D3),
        row_pins=(board.D7, board.D8, board.D9),
        columns_to_anodes=DiodeOrientation.ROW2COL
    ),
    KeysScanner(
        pins=[board.D10],
        value_when_pressed=False,
    ),
]

encoder = AnalogEncoder(
    pin=board.A0,
    thresholds=[1270, 10000, 40000],
    cw=KC.VOLU,
    ccw=KC.VOLD
)

keyboard.modules.append(encoder)


# OLED
i2c = busio.I2C(board.SCL, board.SDA)

driver = SSD1306(i2c=i2c)

display = Display(
    display=driver,
    width=128,
    height=32
)

display.entries = [
    TextEntry(text="ShadyPad", x=0, y=0),
    TextEntry(text="Ready", x=0, y=12),
]

keyboard.extensions.append(display)


keyboard.keymap = [
    [
        KC.A, KC.B, KC.C,
        KC.D, KC.E, KC.F,
        KC.G, KC.H, KC.I,
        KC.MUTE
    ]
]


if __name__ == "__main__":
    keyboard.go()
