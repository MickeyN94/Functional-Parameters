from nicegui.elements.input import Input
from nicegui.elements.number import Number
from nicegui.elements.checkbox import Checkbox
from nicegui.elements.select import Select


class NamedInput(Input):

    def __init__(self, label, value="", name="", on_change=None):
        super().__init__(label=label, value=value, on_change=on_change)

        self.name = name
        self.props('style="width: 120px"')


class NamedNumber(Number):

    def __init__(self, label, value=0, name="", on_change=None):
        super().__init__(label=label, value=value, on_change=on_change)
        self.props('style="width: 150px"')

        self.name = name
        


class NamedCheckbox(Checkbox):

    def __init__(self, text, value=False, name="", on_change=None):
        super().__init__(text=text, value=value, on_change=on_change)

        self.name = name


class NamedSelect(Select):

    def __init__(self, options, label="", name=""):
        super().__init__(options=options, label=label)

        self.name = name
        self.props('style="width: 130px"')