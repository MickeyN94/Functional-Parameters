import math
import os
import csv

def bolt_force(pressure_od, pressure_id, pressure, force):
    if force == 0:
        pressure_area = (pressure_od ** 2 - pressure_id ** 2) * math.pi / 4
        force = pressure_area * pressure * 0.1
    
    return force
    

def tensile_stress(force, number_of_bolts, thread, stress_area, engagement=1):
    thread_data = get_thread_data(thread)
    tensile_stress_area = float(thread_data[stress_area])
    
    return force / (number_of_bolts * tensile_stress_area * engagement)


def safety_factor(material, force, number_of_bolts, thread, stress_area, 
                  engagement=1, thread_stripping=False, yield_sf=True):
    material_data = get_material_data(material)
    if yield_sf:
        material_stress = float(material_data[1])
    else:
        material_stress = float(material_data[2])
        
    stress = tensile_stress(force, number_of_bolts, thread, stress_area, engagement)
    
    if thread_stripping:
        return material_stress * 0.577 / stress
    else:
        return material_stress / stress

def get_thread_types():
    cwd = os.getcwd()
    with open(f'{cwd}\\bolting\calcs\data\metric_threads.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        
        return [row[0] for row in reader]
    
def get_thread_data(thread):
    cwd = os.getcwd()
    with open(f'{cwd}\\bolting\calcs\data\metric_threads.csv') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)
        
        for row in reader:
            if row[0] == thread:
                return dict(zip(headers, row))


def get_material_data(material):
    cwd = os.getcwd()
    with open(f'{cwd}\\bolting\calcs\data\materials.csv') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            if row[0] == material:
                return row


def get_materials():
    cwd = os.getcwd()
    with open(f'{cwd}\\bolting\calcs\data\materials.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        
        return [row[0] for row in reader]


def tensile_stress_tensile_area(force, number_of_bolts, thread):
    return tensile_stress(force, number_of_bolts, thread, 'Tensile Stress Area (mm2)')


def tensile_stress_tensile_root_area(force, number_of_bolts, thread):
    return tensile_stress(force, number_of_bolts, thread, 'Thread Root Area (mm2)')


def tensile_stress_tensile_stripping_area_external(force, number_of_bolts, thread, engagement):
    return tensile_stress(force, number_of_bolts, thread, 
                          'Thread Stripping Area (External) (mm2/mm)', engagement)


def tensile_stress_tensile_stripping_area_internal(force, number_of_bolts, thread, engagement):
    return tensile_stress(force, number_of_bolts, thread, 
                          'Thread Stripping Area (Internal) (mm2/mm)', engagement)


def yield_sf_tensile_area(material, force, number_of_bolts, thread):
    return safety_factor(material, force, number_of_bolts, thread,
                         'Tensile Stress Area (mm2)')


def yield_sf_tensile_root_area(material, force, number_of_bolts, thread):
    return safety_factor(material, force, number_of_bolts, thread,
                         'Thread Root Area (mm2)')


def yield_sf_tensile_stripping_area_external(material, force, number_of_bolts,
                                             thread, engagement):
    return safety_factor(material, force, number_of_bolts, thread,
                         'Thread Stripping Area (External) (mm2/mm)', engagement=engagement,
                         thread_stripping=True)


def yield_sf_tensile_stripping_area_internal(material, force, number_of_bolts,
                                             thread, engagement):
    return safety_factor(material, force, number_of_bolts, thread,
                         'Thread Stripping Area (Internal) (mm2/mm)', engagement=engagement,
                         thread_stripping=True)


def uts_sf_tensile_area(material, force, number_of_bolts, thread):
    return safety_factor(material, force, number_of_bolts, thread,
                         'Tensile Stress Area (mm2)', yield_sf=False)


def uts_sf_tensile_root_area(material, force, number_of_bolts, thread):
    return safety_factor(material, force, number_of_bolts, thread,
                         'Thread Root Area (mm2)', yield_sf=False)


def uts_sf_tensile_stripping_area_external(material, force, number_of_bolts,
                                             thread, engagement):
    return safety_factor(material, force, number_of_bolts, thread,
                         'Thread Stripping Area (External) (mm2/mm)', engagement=engagement,
                         thread_stripping=True, yield_sf=False)


def uts_sf_tensile_stripping_area_internal(material, force, number_of_bolts,
                                             thread, engagement):
    return safety_factor(material, force, number_of_bolts, thread,
                         'Thread Stripping Area (Internal) (mm2/mm)', engagement=engagement,
                         thread_stripping=True, yield_sf=False)
    
    
# print(tensile_stress_tensile_area(17436.6, 1, "M16x2"))
# print(tensile_stress_tensile_root_area(17436.6, 1, "M16x2"))
# print(tensile_stress_tensile_stripping_area_external(17436.6, 1, "M16x2", 12))
# print(tensile_stress_tensile_stripping_area_internal(17436.6, 1, "M16x2", 12))
# print(yield_sf_tensile_area("CW307G", 17436.6, 1, "M16x2"))
# print(yield_sf_tensile_root_area("CW307G", 17436.6, 1, "M16x2"))
print(yield_sf_tensile_stripping_area_external("CW307G", 17436.6, 1, "M16x2", 12))
# print(yield_sf_tensile_stripping_area_internal("CW307G", 17436.6, 1, "M16x2", 12))
# print(uts_sf_tensile_area("CW307G", 17436.6, 1, "M16x2"))
# print(uts_sf_tensile_root_area("CW307G", 17436.6, 1, "M16x2"))
# print(uts_sf_tensile_stripping_area_external("CW307G", 17436.6, 1, "M16x2", 12))
# print(uts_sf_tensile_stripping_area_internal("CW307G", 17436.6, 1, "M16x2", 12))

# safety_factor(material, force, number_of_bolts, thread, stress_area, 
                #   engagement=1, thread_stripping=False, yield_sf=True)


    