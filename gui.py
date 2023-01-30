from nicegui import ui
from all_orings import AllORings
from oring_row import OringRow
from tkinter.filedialog import asksaveasfilename, askopenfilename
import json


def save():
    filename = asksaveasfilename(title="Select your file")
    file = {row.name.value : row.get_attributes() for row in OringRow.instances}
    with open(f'{filename}.json', 'w') as fp:
        json.dump(file, fp)
        
def load():
    filename = askopenfilename(title = "Select your file")
    with open(filename, 'r') as fp:
        d = json.load(fp)
        
    for i in range(len(OringRow.instances)):
        all_orings.remove(0)
        
    for row in d.values():
        new_row = all_orings.add_oring_row()
        new_row.set_attributes(row)
        print(type(row['oring_size']))


all_orings = AllORings()
with ui.row():
    ui.button("Save", on_click=save)
    ui.button("Load", on_click=load)

ui.run()




        
