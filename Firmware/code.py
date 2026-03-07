import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.RGB import RGB
from kmk.extensions.rgb import AnimationModes
from kmk.modules.layers import Layers

from kmk.scanners.keypad import MatrixScanner
from kmk.scanners.keypad import KeysScanner
from kmk.modules import Module
import analogio
from kmk.extensions.media_keys import MediaKeys


class AnalogResistorEncoder(Module):
    def __init__(self, pin, thresholds, cw_key, ccw_key):
        self.pin = pin
        self.thresholds = thresholds
        self.cw_key = cw_key
        self.ccw_key = ccw_key

        self.ain = None
        self.last_state = None

    def during_bootup(self, keyboard):
        self.ain = analogio.AnalogIn(self.pin)
        return

    def before_matrix_scan(self, keyboard):
        val = self.ain.value
        state = self._state_from_adc(val)

        # Debug on state change
        if self.last_state is None:
            print("Initial state:", state, "ADC:", val)

        elif state != self.last_state:
            print("STATE CHANGE:", self.last_state, "→", state, "ADC:", val)

            # Only detect transitions FROM state 3
            if self.last_state == 3:
                if state == 2:
                    keyboard.tap_key(self.ccw_key)
                elif state == 1:
                    keyboard.tap_key(self.cw_key)

        self.last_state = state
        return keyboard

    #
    # Helper
    #

    def _state_from_adc(self, val):
        for i, t in enumerate(self.thresholds):
            if val < t:
                return i
        return len(self.thresholds)

    #
    # Required no-op hooks
    #

    def after_matrix_scan(self, keyboard):
        return keyboard

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

class ShadyPad(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # create and register the scanner
        self.matrix = [
            MatrixScanner(
                column_pins=(board.D1, board.D2, board.D3),
                row_pins=(board.D7, board.D8, board.D9),
                columns_to_anodes=DiodeOrientation.ROW2COL
            ),
            KeysScanner(
                #rotary encoder single key scanner
                pins=[board.D10],
                value_when_pressed=False,
            ),
        ]
    
keyboard = ShadyPad()
keyboard.extensions.append(MediaKeys())

encoder = AnalogResistorEncoder(
    pin=board.A0,
    thresholds=[1270, 10000, 40000],
    cw_key=KC.VOLU,
    ccw_key=KC.VOLD,
)

keyboard.modules.append(encoder)

LEDON = True

class LayerRGB(RGB):
    def on_layer_change(self, layer):
        if LEDON:
            if layer == 0:
                self.set_hsv_fill(79, self.sat_default, self.val_default)   # 
            elif layer == 1:
                self.set_hsv_fill(170, self.sat_default, self.val_default) # blue
            elif layer == 2:
                self.set_hsv_fill(20, self.sat_default, self.val_default) # 
            elif layer == 3:
                self.set_hsv_fill(180, self.sat_default, self.val_default) # 
            elif layer == 4:
                self.set_hsv_fill(225, self.sat_default, self.val_default) # 
            elif layer == 5:
                self.set_hsv_fill(0, 0, self.val_default) # 
        else:
                self.set_hsv_fill(0, 0, 0) # off

        if layer == 6:
            self.set_hsv_fill(0, 0, 0)
            self.set_hsv(0, self.sat_default, 100 if LEDON else 40 , 8) # 
            self.set_hsv(0, self.sat_default, 30 if LEDON else 10, 3)
        self.show()

    def on_layer_change_flash(self):
        if LEDON:
            self.set_hsv_fill(0, 255, 15)
        else:
            self.set_hsv_fill(0, 255, 10)
        self.show()

rgb = LayerRGB(
    pixel_pin=board.D6,
    num_pixels=9,
    hue_default=79,
    sat_default=255,
    val_default=67,
)

keyboard.extensions.append(rgb)

class RGBLayers(Layers):
    def __init__(self):
        super().__init__()
        self.lay = 0
    def activate_layer(self, keyboard, layer, idx=None):
        super().activate_layer(keyboard, layer, idx)
        if(layer != 6):
            rgb.on_layer_change_flash()
            time.sleep(0.15)
            self.lay= layer
        rgb.on_layer_change(layer)

    def deactivate_layer(self, keyboard, layer):
        super().deactivate_layer(keyboard, layer)
        rgb.on_layer_change_flash()
        rgb.on_layer_change(keyboard.active_layers[0])


keyboard.modules.append(RGBLayers())

layers = RGBLayers()
keyboard.modules.append(layers)
from kmk.modules.macros import Delay, Press, Release, Tap
from kmk.modules.macros import Macros
macros = Macros()
keyboard.modules.append(macros)
from kmk.keys import KC

MAC1 = KC.MACRO("I am gonna fallout")

MAC2 = KC.MACRO(
    " 67 "
)


MUTE = KC.MACRO(
    Press(KC.RALT),
    Press(KC.RSHIFT),
    Tap(KC.M),
    Release(KC.RALT),
    Release(KC.RSHIFT)
)

DEAF = KC.MACRO(
    Press(KC.RALT),
    Press(KC.RSHIFT),
    Tap(KC.D),
    Release(KC.RALT),
    Release(KC.RSHIFT)
)

VOLDN = KC.MACRO(
    Press(KC.RALT),
    Tap(KC.PIPE),
    Release(KC.RALT)
)

VOLUP = KC.MACRO(
    Press(KC.RCTRL),
    Press(KC.RALT),
    Tap(KC.PIPE),
    Release(KC.RALT),
    Release(KC.RCTRL)
)

PIF3 = KC.MACRO(
    Press(KC.LSHIFT),
    Tap(KC.F3),
    Release(KC.LSHIFT)
)

DEC = KC.MACRO(
    Press(KC.LSHIFT),
    Press(KC.F3),
    Tap(KC.F),
    Release(KC.F3),
    Release(KC.LSHIFT)
)

INC = KC.MACRO(
    Press(KC.F3),
    Tap(KC.F),
    Release(KC.F3)
)

COP = KC.MACRO(
    Press(KC.LSHIFT),
    Press(KC.LGUI),
    Tap(KC.F23),
    Release(KC.LGUI),
    Release(KC.LSHIFT)
)

TERM = KC.MACRO(
    
    Tap(KC.LGUI),
    "term",
    Tap(KC.ENT)
)

SPEC = KC.MACRO(
    "shut\n"
    "the fuck up\n"    
)


from kmk.extensions.display import Display, TextEntry, ImageEntry
from kmk.modules.holdtap import HoldTap
holdtap = HoldTap()
# optional: set a custom tap timeout in ms
# holdtap.tap_time = 300
keyboard.modules.append(holdtap)


from kmk.keys import Key

rotaryMute = True

img1 = "sound16.bmp"
img2 = "play16.bmp"
# textdisp = TextEntry(text= txt1, x=101, y=0, layer=None)
icondisp = ImageEntry(image="sound16.bmp", x=112)
class RotKey(Key):
   
    def __init__ (self, key1, key2):
        self.key = key1
        self.altkey = key2

    def on_press(self, keyboard, coord_int = None):
        if rotaryMute:
            keyboard.add_key(self.key)
        else:
            keyboard.add_key(self.altkey)

    def on_release(self, keyboard, coord_int = None):
        if rotaryMute:
            keyboard.remove_key(self.key)
        else:
            keyboard.remove_key(self.altkey)

class RotSwap(Key):
    def on_press(self, keyboard, coord_int = None):
        # print("swapped")
        
        global rotaryMute
        rotaryMute = not rotaryMute
        global icondisp
        icondisp.setImage(img1 if rotaryMute else img2)
        display.render(layers.lay)
        print(rotaryMute)

class LedTog(Key):
    def on_press(self, keyboard, coord_int = None):
        global LEDON
        LEDON = not LEDON
        
encTap = RotKey(KC.MUTE, KC.MPLY)
encHold = RotSwap()
rgbtog = LedTog()

ENCP = KC.HT(encTap, encHold, prefer_hold=True, tap_interrupted=False, tap_time=300)

MODE = KC.HT(KC.ENTER, KC.MO(6), prefer_hold= True, tap_time=180, )
MODE1 = KC.HT(KC.N9, KC.MO(6), prefer_hold= True, tap_time=180, )
# --- MEME KEYMAP ---
keyboard.keymap = [
    # Default
    [
        MAC1, MAC2, KC.SPACE,
        VOLDN, KC.MPLY, VOLUP,
        MUTE, DEAF, MODE,
        ENCP
    ],
    # speedrun
    [
        DEC, INC, PIF3,
        VOLDN, KC.MPLY, VOLUP,
        MUTE, DEAF, MODE,
        ENCP
    ],
    # EDITING
    [
        COP, TERM, PIF3,
        VOLDN, KC.MPLY, VOLUP,
        MUTE, DEAF, MODE,
        ENCP
    ],
    # custom 1
    [
        KC.A, KC.S, SPEC,
        KC.NO, KC.K, KC.L,
        KC.SPC, KC.SPC, MODE,
        ENCP
    ],
    # custom 2
    [
        KC.RGB_MODE_RAINBOW, KC.RGB_ANI, KC.RGB_AND,
        KC.RGB_MODE_PLAIN, KC.NO, KC.NO,
        KC.NO, KC.NO, MODE,
        ENCP
    ],
    # numpad
    [
        KC.N1, KC.N2, KC.N3,
        KC.N4, KC.N5, KC.N6,
        KC.N7, KC.N8, MODE1,
        ENCP
    ],
    # redirect
    [
        KC.TO(0), KC.TO(1), KC.TO(2),
        KC.TO(3), KC.TO(4), KC.TO(5),
        KC.NO, rgbtog, KC.TRNS,
        KC.RELOAD
    ]

]


import busio, time



# For SSD1306
from kmk.extensions.display.ssd1306 import SSD1306

# Replace SCL and SDA according to your hardware configuration.
i2c_bus = busio.I2C(board.SCL, board.SDA)

driver = SSD1306(
    # Mandatory:
    i2c=i2c_bus,
)

display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=32, # screen size
    flip = False, # flips your display content
    flip_left = False, # flips your display content on left side split
    flip_right = False, # flips your display content on right side split
    brightness=0.4, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    dim_time=20, # time in seconds to reduce screen brightness
    dim_target=0.01, # set level for brightness decrease
    off_time=600, # time in seconds to turn off screen
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.001, # set level for brightness decrease
    # powersave_off_time=30, # time in seconds to turn off screen
)

display.entries = [
    # ImageEntry(image="cornerDebug.bmp", x=0, y=0),

    # ImageEntry(image="InvRoll.bmp", x=5, y=0),'

    TextEntry(text="Shadypad v1", x=0, y=0),
    icondisp,
    TextEntry(text="Default", x=0, y=12, layer=0), 
    TextEntry(text="Speedrun", x=0, y=12, layer=1),
    TextEntry(text="Editing", x=0, y=12, layer=2),
    TextEntry(text="Osu Geo", x=0, y=12, layer=3),
    TextEntry(text="Custom 2", x=0, y=12, layer=4),
    TextEntry(text="Numpad", x=0, y=12, layer=5),
    TextEntry(text="Mode Swap", x=0, y=12, layer=6),
    # TextEntry(text="Hey there!", x=0, y=24),
]
keyboard.extensions.append(display)


if __name__ == "__main__":
    
    keyboard.go()