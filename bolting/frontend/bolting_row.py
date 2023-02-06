from nicegui import ui
from bolting.calcs.bolting_calcs import *
from utilities.functionalRow import FunctionalRow
from utilities.buttons import NamedCheckbox, NamedInput, NamedNumber, NamedSelect

class BoltingRow(FunctionalRow):
    instances = []
    
    def __init__(self):
        super().__init__()
        thread_types = get_thread_types()
        materials = get_materials()
        BoltingRow.instances.append(self)
        
        with self:
            self.name_label = NamedInput("Label", value="A", name="name_label")
            self.thread_type = NamedSelect(thread_types, label="Thread type", name="thread_type")
            self.engagement = NamedNumber("Thread Engagement", value=0, name="engagement")
            self.number_of_bolts = NamedNumber("Number of Bolts", value=0, name="number_of_bolts")
            self.bolt_material = NamedSelect(materials, label="Bolt Material", name="bolt_material")
            self.nut_material = NamedSelect(materials, label="Nut Material", name="nut_material")
            self.pressure_od = NamedNumber("Pressure OD", value=0, name="pressure_od")
            self.pressure_id = NamedNumber("Pressure ID", value=0, name="pressure_id")
            self.pressure = NamedNumber("Pressure", value=0, name="pressure")
            self.torque_nut_factor = NamedNumber("Torque Nut Factor", value=0.18, name="torque_nut_factor")