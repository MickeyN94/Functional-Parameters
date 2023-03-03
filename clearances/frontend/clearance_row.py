from nicegui import ui
from utilities.functionalRow import FunctionalRow
from utilities.buttons import NamedInput, NamedNumber


class ClearanceRow(FunctionalRow):
    instances = []

    def __init__(self):
        super().__init__()

        ClearanceRow.instances.append(self)
        with self:
            self.name_label = NamedInput("Label", value="A", name="name_label")
            self.bore_dia = NamedNumber('Bore Diameter', value=73.055,
                                        name="bore_dia")
            self.bore_dia_tol = NamedNumber('Bore Diameter Tolerance',
                                            value=0.025, name="bore_dia_tol")
            self.clearance = NamedNumber('Radial Clearance', value=0.075,
                                         name="clearance")
            self.piston_dia_tol = NamedNumber('Piston Diameter Tolerance',
                                              value=0.025,
                                              name="piston_dia_tol")
            ui.button("Remove", on_click=self.delete_row)

        self.all_dimensions = [self.name_label, self.bore_dia, self.bore_dia_tol,
                               self.clearance, self.piston_dia_tol]
            
        
    def get_inventor_assembly_parameters(self):
        piston_dia = self.bore_dia.value - self.clearance.value * 2
                
        d = {f'{self.name_label.value}_{self.bore_dia.name}' : self.bore_dia.value,
             f'{self.name_label.value}_piston_dia' : piston_dia}
                
        return d
    
    def get_inventor_clearance_table_data(self):
        max_clearance = (self.clearance.value + self.bore_dia_tol.value / 2 + self.piston_dia_tol.value / 2) * 1000
        min_clearance = (self.clearance.value - self.bore_dia_tol.value / 2 - self.piston_dia_tol.value / 2) * 1000
        return [self.name_label.value, round(self.bore_dia.value - self.clearance.value * 2,2), round(self.piston_dia_tol.value,2),
                round(self.bore_dia.value,2), round(self.bore_dia_tol.value,2), round(max_clearance,2), round(min_clearance, 2)]
