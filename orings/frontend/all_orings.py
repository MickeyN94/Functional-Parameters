from nicegui import ui
from nicegui.elements.column import Column
from utilities.functionalAllRows import FunctionalAllRows

from orings.frontend.oring_row import OringRow
from utilities.buttons import NamedCheckbox

class AllORings(FunctionalAllRows):
    
    def __init__(self):
        super().__init__(OringRow, "O-ring / Clearance Calcs")
        

        with ui.row().bind_visibility_from(self.rows_active, "value"):
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



# class AllORings(Column):
    
#     def __init__(self):
#         super().__init__()
        
#         with self:
#             self.oring_dynamic = NamedCheckbox("O-ring Calcs", value=True,
#                                                name="oring_dynamic")              
#             OringRow().bind_visibility_from(self.oring_dynamic, "value")

#         with ui.row().bind_visibility_from(self.oring_dynamic, "value"):
#             ui.button("Add Row", on_click=self.add_oring_row)
#             ui.button("Calculate All", on_click=self.calculate_all)
#             ui.button("Calculate Total Friction Force", on_click=self.total_friction)
    
    
#     def save_orings(self):
#         file = {row.name_label.value : row.get_attributes() for row in OringRow.instances}
#         return {"o-rings": file}


#     def load_orings(self, d):
#         d = d['o-rings']
#         for i in range(len(OringRow.instances)):
#             self.remove(1)
#             del OringRow.instances[0]
            
#         for row in d.values():
#             new_row = self.add_oring_row()
#             new_row.set_attributes(row)
            

#     def add_oring_row(self):
#         with self:
#             new_row = OringRow().bind_visibility_from(self.oring_dynamic, "value")
#         return new_row
    
    
#     def calculate_all(self):
#         for row in OringRow.instances:
#             row.calculate()
    
    
#     def total_friction(self):
#         self.calculate_all()
#         try:
#             max_friction_force = sum([row.max_friction_force for row in OringRow.instances if row.dynamic.value])
#             min_friction_force = sum([row.min_friction_force for row in OringRow.instances if row.dynamic.value])
#             force_str = f"Total Friction Force = {max_friction_force:.2f} - {min_friction_force:.2f} N"
#         except:
#             # No dynamic components selected so no friction
#             force_str = "Total Friction Force = 0N (No dynamic components selected"

#         try:
#             self.friction_label.set_text(force_str)
#         except:
#             with self:
#                 self.friction_label = ui.label(force_str)
