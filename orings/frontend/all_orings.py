from nicegui import ui
from nicegui.elements.column import Column
from utilities.functionalAllRows import FunctionalAllRows

from orings.frontend.oring_row import OringRow
from utilities.buttons import NamedCheckbox


class AllORings(FunctionalAllRows):

    def __init__(self):
        super().__init__(OringRow, "O-ring Calcs")

        with ui.row():
            ui.button("Calculate All", on_click=self.calculate_all)
            ui.button("Calculate Total Friction Force", on_click=self.total_friction)

    def calculate_all(self):
        for row in OringRow.instances:
            row.calculate()

    def total_friction(self):
        self.calculate_all()
        try:
            max_friction_force = sum([row.max_friction_force for row in OringRow.instances if row.dynamic.value])
            min_friction_force = sum([row.min_friction_force for row in OringRow.instances if row.dynamic.value])
            force_str = f"Total Friction Force = {max_friction_force:.2f} - {min_friction_force:.2f} N"
        except:
            # No dynamic components selected so no friction
            force_str = "Total Friction Force = 0N (No dynamic components selected"

        try:
            self.friction_label.set_text(force_str)
        except:
            with self:
                self.friction_label = ui.label(force_str)

    
    def get_all_inventor_oring_table_data(self):
        headings = ["Location", "Groove Ø Nom", "Groove Ø Tol",
                    "Groove Width Nom", "Groove Width Tol",
                    "Back-up Ring Thickness", "BS1806 Size",
                    "O-ring Stretch Max %", "O-ring Stretch Min %",
                    "Compression Max %", "Compression Min %",
                    "Gland Fill Max %", "Gland Fill Min %",
                    "Friction Max (N)"]
        title = "O-RING CALCS"
        column_widths = [1.70, 1.6, 1.6, 1.6, 1.6, 1.96, 1.56, 1.54, 1.54,
                         2.51, 2.51, 1.5, 1.5, 1.63 ]
        contents = []
        for row in OringRow.instances:
            contents.extend(row.get_inventor_oring_table_data())
        
        return title, headings, contents, column_widths

    
    def get_all_inventor_clearance_table_data(self):
        contents = []
        for row in OringRow.instances:
            contents.extend(row.get_inventor_clearance_table_data())
        return contents
