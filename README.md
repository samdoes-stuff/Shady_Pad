# Shady Pad
It is 3x3 custom sized 8 key macropad for app shortcuts equipped with a 0.91 inch display and EC11 encoder

## Usage
To use, one should flash their xiao rp2040 with the correct circuitpython .uf2 file, upload the code file, as well as libraries and linked images, save, and you're good to go! you can customize what each key does, lighting color, text displays, etc all within the code.py file

## Cad
<img width="508" height="536" alt="Screenshot 2026-03-07 223007" src="https://github.com/user-attachments/assets/243acd49-7fd8-4457-9b06-e05fa7376c4e" />
<img width="774" height="340" alt="Screenshot 2026-03-07 000336" src="https://github.com/user-attachments/assets/58ce2c62-c9b6-4e0c-a1d4-3dbde6b747e1" />
<img width="682" height="497" alt="Screenshot 2026-03-07 000058" src="https://github.com/user-attachments/assets/61a977f0-8362-409d-88ae-f01fd0ae91b5" />


## PCB

<img width="749" height="585" alt="Screenshot 2026-03-07 161812" src="https://github.com/user-attachments/assets/aed17c88-594f-4b6c-bc01-f3c1acefb0af" />
<img width="735" height="592" alt="Screenshot 2026-03-07 161846" src="https://github.com/user-attachments/assets/ddcd34ff-0c48-401a-b4eb-af40c27cb1ed" />
<img width="658" height="574" alt="Screenshot 2026-03-07 161907" src="https://github.com/user-attachments/assets/bf7f4f5a-349e-4ded-93fc-130156205f6f" />
<img width="742" height="553" alt="Screenshot 2026-03-07 161943" src="https://github.com/user-attachments/assets/989d2a46-9907-4fc3-8513-6aba0c7adad9" />


## Schematic

<img width="983" height="661" alt="Screenshot 2026-03-07 162502" src="https://github.com/user-attachments/assets/37fdc754-c5b9-4c50-ac79-98cb6da6ed24" />


I later did not used LEDs in my PCB
## Firmware
- KMK based,
- Screen used for identifying layers, icon display, and signature display
- Custom rotary encoder decoding software from one analog pin
- Custom Key object designed for the rotary encoder multi function button
- Advanced use of macros and hotkeys for daily use
## BOM
Please refer to BOM.csv
