from win32com.client import VARIANT
from inventor_files.inventorAll import Inventor
from pythoncom import VT_ARRAY, VT_BSTR, VT_R8

class InventorDrawing(Inventor):
    
    def __init__(self):
        super().__init__()
    
        self.drawing_doc = self.mod.DrawingDocument(self.doc)

    def create_table(self, title, headings, contents, column_widths):
        
        sheet = self.drawing_doc.ActiveSheet
        tables = sheet.CustomTables
        columns = len(headings)
        rows = len(contents) / len(headings)
        contents = self.variant_string(contents)
        column_widths = self.variant_float(column_widths)
        x, y = 10, 10
        
        # headings = ["part_num", "quantity"]
        # contents = self.variant(["Y02", 2, "Y013", "4"])
        # contents2 = self.variant(["Y02", 2, "test", "test2"])
        # default_placement = self.app.TransientGeometry.CreatePoint2d(5,10)

        if tables.Count > 0:
            for i in range(tables.Count):
                if tables.Item(i + 1).Title == title:
                    table = tables.Item(i + 1)
                    x = table.RangeBox.MinPoint.X
                    y = table.RangeBox.MaxPoint.Y
                    table.Delete()
                    break

            
        placement = self.app.TransientGeometry.CreatePoint2d(x, y)    
        tables.Add(title, placement, columns, rows, headings, contents, ColumnWidths=column_widths)
    
# https://help.autodesk.com/view/INVNTOR/2022/ENU/?guid=CustomTables_Add
# https://help.autodesk.com/view/INVNTOR/2022/ENU/?guid=Sheet_CustomTables
    def variant_string(self, data):
        return VARIANT(VT_ARRAY | VT_BSTR, data)

    def variant_float(self, data):
        return VARIANT(VT_ARRAY | VT_R8, data)