Cubitpad
The Cubitpad is a macropad that is designed to maximize functionality in the smallest footprint. It utilizes all pins to their maximum extent on the Seeeduino XIAO RP2040 for the most features, which includes: NKRO 3x3 macro, rotary encoder with push function, and a 0.91" OLED monochrome screen, the keypad also being backlit with neopixels for some flair

Usage
To use, one should flash their xiao rp2040 with the correct circuitpython .uf2 file, upload the code file, as well as libraries and linked images, save, and you're good to go! you can customize what each key does, lighting color, text displays, etc all within the code.py file

Creation
This was initially created as my own current keyboard lacks a rotary encoder, and I wanted one for volume and other controls, which then spiraled into this project

Image
S__15409169

Cad
image
PCB
image
Schematic
image
Case by itself
image image image Friction fitted (with clearance designed for 3d printing) (I can print this myself, but some filament could be nice)
Firmware
KMK based,
Screen used for identifying layers, icon display, and signature display
Neopixel used for backlight
Custom rotary encoder decoding software from one analog pin
Custom Key object designed for the rotary encoder multi function button
Advanced use of macros and hotkeys for daily use
## BOM
Qty,Item,Notes
1,SEEEDUINO XIAO RP2040,Microcontroller board
9,MX-style switches,5-pin preferred
10,1N4148 through-hole diodes,For switch matrix
1,SSD1306 128x32 OLED 0.91,I2C display
9,Blank DSA keycaps,
1,EC11 rotary encoder,

