from nicegui import ui
from orings.frontend.all_orings import AllORings
from custom_parameter.frontend.all_parameters import AllParameters
from tkinter.filedialog import asksaveasfilename, askopenfilename
from utilities.functionalAllRows import FunctionalAllRows
from bolting.frontend.bolting_row import BoltingRow
import json


def save():
    filename = asksaveasfilename(title="Select your file", 
                                 filetypes=[("JSON file", ".json")],
                                 defaultextension=".json")
    
    if filename:
        file = {}
        for rows in FunctionalAllRows.instances:
            file.update(rows.save())

        with open(filename, 'w') as fp:
            json.dump(file, fp)
    else:
        ui.notify("No file selected")
        
def load():
    filename = askopenfilename(title = "Select your file",
                               filetypes=[("JSON file", ".json")])
    if filename:
        with open(filename, 'r') as fp:
            d = json.load(fp)
        
        for rows in FunctionalAllRows.instances:
            rows.load(d)

    else:
        ui.notify("No file selected")
        

all_orings = AllORings()
all_parameters = AllParameters()
BoltingRow()
with ui.row():
    ui.button("Save", on_click=save)
    ui.button("Load", on_click=load)

ui.run()




        
