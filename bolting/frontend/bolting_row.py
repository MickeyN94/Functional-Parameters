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
            self.nut_material = NamedSelect(materials, label="Nut Material", name="nut_material", )
            self.pressure_od = NamedNumber("Pressure OD", value=0, name="pressure_od")
            self.pressure_id = NamedNumber("Pressure ID", value=0, name="pressure_id")
            self.pressure = NamedNumber("Pressure", value=0, name="pressure")
            self.torque_nut_factor = NamedNumber("Torque Nut Factor", value=0.18, name="torque_nut_factor")
            self.force_check = NamedCheckbox("Input Force", name="force_check",
                                             on_change=self.set_pressure_sizes)
            self.force_set = NamedNumber("Force", value=0, name="force").bind_visibility_from(self.force_check, 'value')

            ui.button("Calculate", on_click=self.calculate)
            ui.button("Remove", on_click=self.delete_row)

        self.all_dimensions = [self.name_label, self.thread_type, self.engagement,
                               self.number_of_bolts, self.bolt_material, self.nut_material,
                               self.pressure_od, self.pressure_id, self.pressure,
                               self.torque_nut_factor, self.force_check, self.force_set]

    def calculate(self):
        force = bolt_force(self.pressure_od.value, self.pressure_id.value,
                           self.pressure.value, self.force_set.value)
         
        self.min_yield_sf = minimum_yield_sf(self.pressure_od.value, self.pressure_id.value, 
                                             self.pressure.value, self.force_set.value, 
                                             self.bolt_material.value, self.nut_material.value, 
                                             self.number_of_bolts.value, self.thread_type.value, self.engagement.value)

        self.min_uts_sf = minimum_uts_sf(self.pressure_od.value, self.pressure_id.value, 
                                             self.pressure.value, self.force_set.value, 
                                             self.bolt_material.value, self.nut_material.value, 
                                             self.number_of_bolts.value, self.thread_type.value, self.engagement.value)        
        self.torque = torque(self.pressure_od.value, self.pressure_id.value, self.pressure.value, 
                             force, self.torque_nut_factor.value, self.thread_type.value, 
                             self.number_of_bolts.value)
        
        self.min_sf = f"Minimum Safety Factors; Yield: {self.min_yield_sf:.2f}, UTS: {self.min_uts_sf:.2f}. Min Torque: {self.torque:.2f} Nm"
        

        try:
            self.min_sf_label.set_text(self.min_sf)
        except:
            with self:
                self.min_sf_label = ui.label(self.min_sf)

    def set_pressure_sizes(self):
        pressure_dims = [self.pressure_od, self.pressure_id, self.pressure]

        if self.force_check.value:
            for dim in pressure_dims:
                dim.value = 0
                dim.set_visibility(False)
        else:
            self.force_set.value = 0
            for dim in pressure_dims:
                dim.set_visibility(True)

    def get_inventor_bolt_table_data(self):
        force = bolt_force(self.pressure_od.value, self.pressure_id.value,
                           self.pressure.value, self.force_set.value)
        params =  [self.name_label.value, self.thread_type.value, self.engagement.value,
                self.number_of_bolts.value, self.bolt_material.value,
                self.nut_material.value, self.pressure_od.value,
                self.pressure_id.value, self.pressure.value, self.torque_nut_factor.value, force,
                self.min_yield_sf, self.min_uts_sf, self.torque]

        params_tidy = []
        for param in params:
            if type(param) == float:
                params_tidy.append(round(param,2))
            else:
                params_tidy.append(param)
        return params_tidy