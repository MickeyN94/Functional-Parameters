from nicegui import ui
from utilities.functionalAllRows import FunctionalAllRows

from bolting.frontend.bolting_row import BoltingRow


class AllBolting(FunctionalAllRows):

    def __init__(self):
        super().__init__(BoltingRow, "Bolting Calcs")
        
          
        ui.button("Calculate All", on_click=self.calculate_all)

    def calculate_all(self):
        for row in BoltingRow.instances:
            row.calculate()
    
    
    def get_all_inventor_bolting_table_data(self):
        headings = ["Location", "Thread Type", "Engagement", "No. of Bolts",
                    "Bolt Material", "Nut Material",
                    "Pressure OD (mm)", "Pressure ID (mm)",
                    "Pressure (Bar)", "Torque Nut Factor",
                    "Force (N)", "Minimum SF Yield",
                    "Minimum SF UTS", "Minimum Torque (Nm)"]
        
        title = "BOLTING CALCS"
        column_widths = [1.70, 1.75, 2.50, 1.27, 1.63, 1.63, 1.89, 1.89, 1.74,
                         1.47, 1.87, 1.84, 1.84, 1.84]
        contents = []
        for row in BoltingRow.instances:
            contents.extend(row.get_inventor_bolt_table_data())
        
        return title, headings, contents, column_widths
