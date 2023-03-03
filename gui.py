from nicegui import ui
from orings.frontend.all_orings import AllORings
from custom_parameter.frontend.all_parameters import AllParameters
from tkinter.filedialog import asksaveasfilename, askopenfilename
from utilities.functionalAllRows import FunctionalAllRows
from bolting.frontend.all_bolting import AllBolting
from clearances.frontend.all_clearances import AllClearances
from inventor_files.inventorAssembly import InventorAssembly
from inventor_files.inventorDrawing import InventorDrawing
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
    filename = askopenfilename(title="Select your file",
                               filetypes=[("JSON file", ".json")])
    if filename:
        with open(filename, 'r') as fp:
            d = json.load(fp)

        for rows in FunctionalAllRows.instances:
            rows.load(d)

    else:
        ui.notify("No file selected")


def export_parameters_to_inventor_assy():
    d = {}
    for rows in FunctionalAllRows.instances:
        if not isinstance(rows, AllBolting):
            d.update(rows.get_all_inventor_assembly_parameters())
    assembly = InventorAssembly()
    assembly.import_parameters(d)


def export_tables_to_inventor():
    all_orings.calculate_all()
    all_bolting.calculate_all()
    drawing = InventorDrawing()
    
    # O-RING CALCS TABLE
    title, heading, contents, column_widths = all_orings.get_all_inventor_oring_table_data()
    drawing.create_table(title, heading, contents, column_widths)

    # CLEARANCE TABLE
    title = "CLEARANCES"
    heading = ["Location", "Piston Ø Nom", "Piston Ø Tol",
                "Bore Ø Max", "Bore Ø Tol", "Max Radial Clearance (µm)",
                "Min Radial Clearance (µm)"]
    
    column_widths = [1.70, 1.43, 1.43, 1.43, 1.43, 2.25, 2.25]
    
    contents = all_orings.get_all_inventor_clearance_table_data()
    contents.extend(all_clearances.get_all_inventor_clearance_table_data())
    drawing.create_table(title, heading, contents, column_widths)
    
    # BOLTING TABLE
    title, heading, contents, column_widths = all_bolting.get_all_inventor_bolting_table_data()
    drawing.create_table(title, heading, contents, column_widths)
    

with ui.tabs() as tabs:
    ui.tab("O-Ring Calcs")
    ui.tab("Clearances")
    ui.tab("Additional Parameters")
    ui.tab("Bolting")
    
# tabs.props('class="bg-primary text-white shadow-2"')

with ui.tab_panels(tabs, value="O-Ring Calcs"):
    with ui.tab_panel('O-Ring Calcs'):
        all_orings = AllORings()
    with ui.tab_panel('Clearances'):
        all_clearances = AllClearances()
    with ui.tab_panel('Additional Parameters'):
        AllParameters()
    with ui.tab_panel('Bolting'):
        all_bolting = AllBolting()   

with ui.row():
    ui.button("Save", on_click=save)
    ui.button("Load", on_click=load)
    ui.button("Export to Inventor", on_click=export_parameters_to_inventor_assy)
    ui.button("Export to Inventor Drawing", on_click=export_tables_to_inventor)

ui.run(title="Functional Parameters",
       host='127.0.0.1',
       show=False, reload=True,)
