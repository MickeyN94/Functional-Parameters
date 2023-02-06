from nicegui import ui
from orings.calcs.compression_calc import total_compression_range
from orings.calcs.gland_fill_calcs import total_gland_fill_range
from orings.calcs.friction_calcs import total_friction_force_range
from utilities.functionalRow import FunctionalRow
from utilities.buttons import NamedCheckbox, NamedInput, NamedNumber

class OringRow(FunctionalRow):
    instances = []
    
    def __init__(self):
        super().__init__()
        
        OringRow.instances.append(self)
        with self:
            self.name_label = NamedInput("Label", value="A", name="name_label") 
            self.bore_dia = NamedNumber('Bore Diameter', value=73.055, 
                                        name="bore_dia")
            self.bore_dia_tol = NamedNumber('Bore Diameter Tolerance', 
                                            value=0.025, name="bore_dia_tol")
            self.groove_dia = NamedNumber('Groove Diameter', value=63.58, 
                                          name="groove_dia")
            self.groove_dia_tol = NamedNumber('Groove Diameter Tolerance', 
                                              value=0.03, name="groove_dia_tol")
            self.groove_width = NamedNumber('Groove Width', value=6, 
                                            name="groove_width")
            self.groove_width_tol = NamedNumber('Groove Width Tolerance', 
                                                value=0.12, name="groove_width_tol")
            self.clearance = NamedNumber('Radial Clearance', value=0.075, 
                                         name="clearance")
            self.piston_dia_tol = NamedNumber('Piston Diameter Tolerance', 
                                              value=0.025, 
                                              name="piston_dia_tol")
            self.oring_type = NamedCheckbox("BS1806 O-ring", value=True,
                                             on_change=self.set_custom_oring_sizes,
                                             name="oring_type")
            self.oring_size = NamedInput('BS1806 O-ring Size', value="333",
                                         name="oring_size").bind_visibility_from(self.oring_type, 'value')
            self.oring_id = NamedNumber("O-ring ID", value = 0, name="oring_id")
            self.oring_id_tol = NamedNumber("O-ring ID Tolerance", value = 0, name="oring_id_tol")
            self.oring_cs_dia = NamedNumber("O-ring Cross-Section Diameter", value = 0, name="oring_cs_dia")
            self.oring_cs_dia_tol = NamedNumber("O-ring Cross-Section Tolerance", value = 0, name="oring_cs_dia_tol")
            self.dynamic = NamedCheckbox("Dynamic", value=False, 
                                         on_change=self.set_friction_parameters, 
                                         name="dynamic")
            self.hardness = NamedNumber("O-ring Hardness", value = 70, 
                                        name="hardness").bind_visibility_from(self.dynamic, 'value')
            self.coef_of_friction = NamedNumber("Coefficient of Friction", 
                                                value = 0.4, 
                                                name="coef_of_friction").bind_visibility_from(self.dynamic, 'value') 
            self.backup_ring = NamedCheckbox("Back-up Ring", value=False, 
                                             on_change=self.set_backup_ring_thickness_0, 
                                             name="backup_ring")
            self.backup_ring_thickness = NamedNumber("Back-up Ring Thickness", 
                                                     value=0, 
                                                     name="backup_ring_thickness").bind_visibility_from(self.backup_ring, 'value')
            ui.button("Calculate", on_click=self.calculate)
            ui.button("Remove", on_click=self.delete_row)
        
        self.all_dimensions = [self.name_label, self.bore_dia, self.bore_dia_tol, 
                                 self.groove_dia, self.groove_dia_tol, self.groove_width,
                                 self.groove_width_tol, self.clearance, self.piston_dia_tol,
                                 self.oring_size, self.dynamic, self.hardness,
                                 self.coef_of_friction, self.backup_ring,
                                 self.backup_ring_thickness, self.oring_id, self.oring_id_tol,
                                 self.oring_cs_dia, self.oring_cs_dia_tol, self.oring_type]
        self.set_custom_oring_sizes()

    
    def calculate(self): 
        self.compression_calc()
        self.gland_fill_calc()
        if self.dynamic.value:
            self.friction_force_calc()
        else:
            if hasattr(self, "friction_label"):
                self.remove(self.friction_label)

        
    def compression_calc(self):
        comp = total_compression_range(self.bore_dia.value, self.bore_dia_tol.value, self.groove_dia.value,
                                       self.groove_dia_tol.value, self.get_oring_parameters())
        
        self.max_comp = comp["max_comp"]
        self.min_comp = comp["min_comp"]
        
        comp_str = f"Compression: {self.max_comp:.2f}-{self.min_comp:.2f}%"
        
        try:
            self.comp_label.set_text(comp_str)
        except:
            with self:
                self.comp_label = ui.label(comp_str)

    
    def gland_fill_calc(self):
        fill = total_gland_fill_range(self.bore_dia.value, self.bore_dia_tol.value,
                                      self.groove_dia.value, self.groove_dia_tol.value,
                                      self.groove_width.value, self.groove_width_tol.value,
                                      self.get_oring_parameters(), self.backup_ring_thickness.value)
        
        self.max_fill = fill["max_fill"]
        self.min_fill = fill["min_fill"]
        
        fill_str = f"Gland Fill: {self.max_fill:.2f}-{self.min_fill:.2f}%"
               
        try:
            self.fill_label.set_text(fill_str)
        except:
            with self:
                self.fill_label = ui.label(fill_str)
    
    
    def friction_force_calc(self):
        friction_force = total_friction_force_range(self.bore_dia.value, self.bore_dia_tol.value,
                                           self.groove_dia.value, self.groove_dia_tol.value,
                                           self.get_oring_parameters(), self.hardness.value,
                                           self.coef_of_friction.value)
        
        self.max_friction_force = friction_force["max_friction_force"]
        self.min_friction_force = friction_force["min_friction_force"]
        
        friction_force_str = f"Friction Force: {self.max_friction_force:.2f}-{self.min_friction_force:.2f}N"
        
        try:
            self.friction_label.set_text(friction_force_str)
        except:
            with self:
                self.friction_label = ui.label(friction_force_str)


    def set_backup_ring_thickness_0(self):
        self.backup_ring_thickness.value = 0

    
    def set_friction_parameters(self):
        self.coef_of_friction.value = 0
        self.hardness.value = 0
        self.max_friction_force = 0
        self.min_friction_force = 0
    
    
    def set_custom_oring_sizes(self):
        
        custom_oring_dims = [self.oring_id,
                         self.oring_id_tol,
                         self.oring_cs_dia, 
                         self.oring_cs_dia_tol]
        
        if self.oring_type.value:
            for dim in custom_oring_dims:
                dim.value = 0
                dim.set_visibility(False)
        else:
            self.oring_size.value = 0
            for dim in custom_oring_dims:
                dim.set_visibility(True)
    
    
    def get_oring_parameters(self):
        return (self.oring_type.value, self.oring_size.value, 
                self.oring_id.value, self.oring_cs_dia.value, 
                self.oring_id_tol.value, self.oring_cs_dia_tol.value)
        
    
    # def set_label_text(self, label, text):
        
    #     if hasattr(self, label):
    #         val =selflabel
            
        
    #     try:
    #         label.set_text(text)
    #     except:
    #         with self:
    #             label = ui.label(text)       