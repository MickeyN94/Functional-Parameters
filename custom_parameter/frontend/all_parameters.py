from utilities.functionalAllRows import FunctionalAllRows
from custom_parameter.frontend.parameter_row import ParameterRow


class AllParameters(FunctionalAllRows):
    
    def __init__(self):
        super().__init__(ParameterRow, "Additional Parameters")

