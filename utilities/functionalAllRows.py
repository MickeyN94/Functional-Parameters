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
            self.row_class()

        with ui.row():
            ui.button("Add Row", on_click=self.add_row)

    def save(self):
        try:
            file = {row.name_label.value: row.get_attributes() for row in self.row_class.instances}
            return {self.rows_type: file}
        except AttributeError:
            return {self.rows_type: ""}

    def load(self, d):
        d = d[self.rows_type]

        for i in range(len(self.row_class.instances)):
            self.remove(0)
            del self.row_class.instances[0]

        if d != "":
            for row in d.values():
                new_row = self.add_row()
                new_row.set_attributes(row)

    def add_row(self):
        with self:
            new_row = self.row_class()
        return new_row

    def get_all_inventor_assembly_parameters(self):
        d = {}
        for row in self.row_class.instances:
            d.update(row.get_inventor_assembly_parameters())
        
        return d
    
