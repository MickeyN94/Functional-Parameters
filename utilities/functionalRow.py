from nicegui.elements.row import Row

class FunctionalRow(Row):
    instances = []
    
    def __init__(self):
        super().__init__()
        
        FunctionalRow.instances.append(self)

     
    def delete_row(self):
        
        while True:
            try:
                self.remove(0)
            except IndexError:
                break
    
        self.instances.remove(self)

   
    def get_attributes(self):

        return {dim.name: dim.value for dim in self.all_dimensions}


    def set_attributes(self, d):        
        for dim in self.all_dimensions:
            for k, v in d.items():
                if dim.name == k:
                    dim.value = v