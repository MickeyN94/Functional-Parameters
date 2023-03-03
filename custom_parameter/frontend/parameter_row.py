from nicegui import ui
from utilities.functionalRow import FunctionalRow
from utilities.buttons import NamedInput, NamedNumber

class ParameterRow(FunctionalRow):
    instances = []
    
    def __init__(self):
        super().__init__()
        
        ParameterRow.instances.append(self)
        with self:
            self.name_label = NamedInput("Parameter Name", value="", name="name_label")
            self.parameter_value = NamedNumber("Value", value=0, name="parameter_value")
            ui.button("Remove", on_click=self.delete_row)

        self.all_dimensions = [self.name_label, self.parameter_value]
    
    def get_inventor_assembly_parameters(self):
        return {self.name_label.value : self.parameter_value.value}
        