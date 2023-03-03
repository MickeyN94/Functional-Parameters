import win32com.client
from win32com.client import gencache


class Inventor():
    
    def __init__(self):
        
        # returns the active document.. Can be updated to select a file 
        try:
            self.app = win32com.client.GetActiveObject('Inventor.Application')
        except:
            self.app = win32com.client.Dispatch('Inventor.Application')
            self.app.Visible = True
        
        self.mod = gencache.EnsureModule('{D98A091D-3A0F-4C3E-B36E-61F62068D488}', 0, 1, 0)
        inv_app_com = self.mod.Application(self.app)
        self.doc = inv_app_com.ActiveDocument     