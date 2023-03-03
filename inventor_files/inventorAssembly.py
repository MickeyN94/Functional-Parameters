import win32com.client
from win32com.client import gencache, VARIANT
from inventor_files.inventorAll import Inventor
from pythoncom import VT_ARRAY, VT_BSTR
import os

class InventorAssembly(Inventor):
    
    def __init__(self):
        super().__init__()
                   
        self.part_doc = self.mod.PartDocument(self.doc)
    
    def import_parameters(self, d):
        editable_parts = self.get_editable_components()
        for path in editable_parts:
            for k,v in d.items():
                self.add_custom_parameter(k, v, path)
    
    def add_custom_parameter(self, name, dim, file_path):
        oDoc = self.app.Documents.Open(file_path, False)
        oDoc = self.mod.PartDocument(oDoc)
        paras = oDoc.ComponentDefinition.Parameters
        
        try:
            para = paras(name)
            para.Value = dim / 10
        except:
            paras.UserParameters.AddByExpression(name, dim, "mm")
            para = paras(name)

    def get_editable_components(self):
        # returns all the files that are checked-out / not in vault (anything not read-only)
        # inside the assembly
        ref_docs = self.doc.AllReferencedDocuments    
        return [ref_doc.FullDocumentName for ref_doc in ref_docs 
                if os.access(ref_doc.FullDocumentName,os.W_OK)]




# def add_custom_parameter2(name, dim, tolerance):
#     paras = oDoc.ComponentDefinition.Parameters

#     try:
#         para = paras(name)
#         para.Value = dim / 10
#         para.Tolerance.SetToSymmetric(tolerance / 10)
#     except:
#         paras.UserParameters.AddByExpression(name, dim, "mm")
#         para = paras(name)
#         para.Tolerance.SetToSymmetric(tolerance)


    # user_parameters = oDoc.ComponentDefinition.Parameters.UserParameters
    # try:
    #     param = user_parameters.Item(name)
    #     param.Expression = dim
    #     param.Tolerance.SetToSymmetric(0.5)
    # except:
    #     user_parameters.AddByExpression(name, dim, "mm")




# prop = oDoc.PropertySets.Item("Design Tracking Properties")
# Descrip = prop('Description').Value
# Designer = prop('Designer').Value
# print(Descrip)
# print(Designer)

# prop = oDoc.PropertySets.Item("Inventor User Defined Properties")
# print(prop('State').Value)
# print(prop('Checked Out By').Value)


# add_custom_parameter("Length", 30, oDoc)
# add_custom_parameter2("d5", 20, 1)
# add_custom_parameter2("Width", 20, 0.5)
# oDoc.Update()

# https://forums.autodesk.com/t5/inventor-ilogic-and-vb-net-forum/how-to-get-parameters-and-mass-of-a-part-with-python/td-p/7553056/highlight/true/page/2

# Table at bottom of the document linking the property with the set.
# https://modthemachine.typepad.com/my_weblog/2010/02/accessing-iproperties.html