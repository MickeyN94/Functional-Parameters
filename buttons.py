from nicegui.elements.input import Input
from nicegui.elements.number import Number
from nicegui.elements.checkbox import Checkbox


class NamedInput(Input):
    
    def __init__(self, label, value="", name="", on_change=None):
        super().__init__(label=label, value=value, on_change=on_change)
        
        self.name = name


class NamedNumber(Number):
    
    def __init__(self, label, value=0, name="", on_change=None):
        super().__init__(label=label, value=value, on_change=on_change)
              
        self.name = name


class NamedCheckbox(Checkbox):
    
    def __init__(self, text, value=False, name="", on_change=None):
        super().__init__(text=text, value=value, on_change=on_change)
        
        
        self.name = name
