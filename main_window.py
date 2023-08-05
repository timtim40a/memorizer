import PySimpleGUI as sg
from argparse import ArgumentParser
from time import sleep
from text_processor import *

parser = ArgumentParser()
parser.add_argument("final_text", type=str)
args = parser.parse_args()

filename = ""

sg.theme("LightBrown4")
mline = sg.Multiline(args.final_text, border_width=4, size=(45, 20), key="-OUTPUT-")

layout = [
    [mline],
    [sg.InputText("file name:", size=(45, 1), key="-IN-")],
    [
        sg.Frame(
            "main_options",
            layout=[
                [
                    sg.Button("Open"),
                    sg.Button("Shuffle"),
                    sg.Button("View Original"),
                    sg.Button("Highlight Epithets", key="-HL-"),
                ],
                [
                    sg.Button("Save Epithets"),
                    sg.Button("Divide Into Sentences", key="-DIVIDE-"),
                ],
            ],
        )
    ],
]

# Create the window
window = sg.Window("Demo", layout)
current_text = ""
hl = False
# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Open":
        filename = window["-IN-"]
    elif event == "Shuffle":
        window["-OUTPUT-"].update(get_final_text())
    elif event == "View Original":
        window["-OUTPUT-"].update(get_raw_text())
    elif event == "-HL-" and not hl:
        hl = True
        current_text = window["-OUTPUT-"].get()
        window["-OUTPUT-"].update(get_highlighted_text(current_text))
        window["-HL-"].update(text="Remove Highlighting")
        window.refresh()
    elif event == "-HL-" and hl:
        hl = False
        window["-OUTPUT-"].update(current_text)
        window["-HL-"].update(text="Highlight Epithets")
        window.refresh()
    elif event == "Save Epithets":
        save_epithets()
    elif event == "-DIVIDE-":
        separate(get_final_text())
    elif event == sg.WIN_CLOSED:
        break

window.close()
