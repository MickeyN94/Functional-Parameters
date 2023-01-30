from nicegui import ui
from nicegui.elements.column import Column
from oring_row import OringRow

class AllORings(Column):
    
    def __init__(self):
        super().__init__()
        
        with self:
            OringRow()

        with ui.row():
            ui.button("Add Row", on_click=self.add_oring_row)
            ui.button("Calculate All", on_click=self.calculate_all)
            ui.button("Calculate Total Friction Force", on_click=self.total_friction)
            

    def add_oring_row(self):
        with self:
            new_row = OringRow()
        return new_row
    
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
            
        ui.label(force_str)