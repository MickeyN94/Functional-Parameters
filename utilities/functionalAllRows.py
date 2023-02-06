from nicegui import ui
from nicegui.elements.column import Column

class FunctionalAllRows(Column):
    instances = []

    def __init__(self, RowClass, rows_name):
        super().__init__()
        self.row_class = RowClass
        self.rows_type = rows_name
        
        FunctionalAllRows.instances.append(self)
        
        with self:
            self.rows_active = ui.checkbox(self.rows_type, value=True)
            
            self.row_class().bind_visibility_from(self.rows_active, "value")
        
        with ui.row().bind_visibility_from(self.rows_active, "value"):
            ui.button("Add Row", on_click=self.add_row)
    
    
    def save(self):
        file = {row.name_label.value : row.get_attributes() for row in self.row_class.instances}
        return {self.rows_type: file}


    def load(self, d):
        d = d[self.rows_type]
        for i in range(len(self.row_class.instances)):
            self.remove(1)
            del self.row_class.instances[0]
            
        for row in d.values():
            new_row = self.add_row()
            new_row.set_attributes(row)
            

    def add_row(self):
        with self:
            new_row = self.row_class().bind_visibility_from(self.rows_active, "value")
        return new_row