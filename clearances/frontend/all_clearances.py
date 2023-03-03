from utilities.functionalAllRows import FunctionalAllRows
from clearances.frontend.clearance_row import ClearanceRow


class AllClearances(FunctionalAllRows):

    def __init__(self):
        super().__init__(ClearanceRow, "Clearances")
        
    
    def get_all_inventor_clearance_table_data(self):
        contents = []
        for row in ClearanceRow.instances:
            contents.extend(row.get_inventor_clearance_table_data())
        return contents