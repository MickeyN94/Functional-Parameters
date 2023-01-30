import csv
import math

def total_compression_range(bore_dia, bore_dia_tol, groove_dia, groove_dia_tol, oring_size):

    bore_dia_max, bore_dia_min = dimension_limits(bore_dia, bore_dia_tol)
    groove_dia_max, groove_dia_min = dimension_limits(groove_dia, groove_dia_tol)

    oring_cs_dia_max, oring_cs_dia_min, oring_id_max, oring_id_min = oring_dims(oring_size)

    max_comp = compression(groove_dia_max, oring_id_max, oring_cs_dia_max, bore_dia_min)
    min_comp = compression(groove_dia_min, oring_id_min, oring_cs_dia_min, bore_dia_max)

    return {"max_comp": max_comp, "min_comp": min_comp}


def compression(groove_dia, oring_id, oring_cs_dia, bore_dia):
    
    oring_cs_dia_reduced = oring_stretched_cs_dia(oring_cs_dia, groove_dia, oring_id)
    return (oring_cs_dia_reduced - ((bore_dia - groove_dia)/2))/oring_cs_dia_reduced * 100


def total_gland_fill_range(bore_dia, bore_dia_tol, groove_dia, groove_dia_tol, 
                     groove_width, groove_width_tol, oring_size, backup_ring_thickness):
    
    groove_dia_max, groove_dia_min = dimension_limits(groove_dia, groove_dia_tol)
    bore_dia_max, bore_dia_min = dimension_limits(bore_dia, bore_dia_tol)
    groove_width_max, groove_width_min = dimension_limits(groove_width, groove_width_tol)
    
    oring_cs_dia_max, oring_cs_dia_min, oring_id_max, oring_id_min = oring_dims(oring_size)
    
    max_fill = gland_fill(groove_dia_max, bore_dia_min, groove_width_min, oring_id_max, oring_cs_dia_max, backup_ring_thickness)
    min_fill = gland_fill(groove_dia_min, bore_dia_max, groove_width_max, oring_id_min, oring_cs_dia_min, backup_ring_thickness)
    
    return {"max_fill": max_fill, "min_fill": min_fill}


def gland_fill(groove_dia, bore_dia, groove_width, oring_id, oring_cs_dia, backup_ring_thickness):
    
    oring_csa = oring_stretched_csa(oring_cs_dia, groove_dia, oring_id)
    groove_area = groove_csa(bore_dia, groove_dia, groove_width, backup_ring_thickness)
    return oring_csa / groove_area * 100


def groove_csa(bore_dia, groove_dia, groove_width, backup_ring_thickness):
    return (bore_dia - groove_dia)/2 * (groove_width - backup_ring_thickness)


def dimension_limits(dimension, tolerance):
    return dimension + tolerance, dimension - tolerance


def oring_dims(oring):
    with open('o-ring_sizes.csv') as csvfile:
        reader = csv.reader(csvfile)

        # check that the oring size given is in BS1806
        sizes = [row[0] for row in reader]
        if str(oring) in sizes:
            # find the row that the oring size matches with from BS1806
            csvfile.seek(0)
            for row in reader:
                if row[0] == str(oring):

                    # convert all values from string to floats to return
                    dims = [float(val) for val in row]
                    break
        else:
            print(f"O-ring size not in BS1806: {oring}")

    _, oring_id, oring_cs_dia, oring_id_tol, o_ring_cs_dia_tol = dims
    oring_cs_dia_max, oring_cs_dia_min = dimension_limits(oring_cs_dia, o_ring_cs_dia_tol)
    oring_id_max, oring_id_min = dimension_limits(oring_id, oring_id_tol)
    
    
    return oring_cs_dia_max, oring_cs_dia_min, oring_id_max, oring_id_min


def oring_stretch(groove_dia, oring_id):
    # returns the % stretch of the oring
    stretch = (groove_dia - oring_id) / oring_id * 100
    if stretch < 0:
        stretch = 0
    return stretch


def oring_cs_dia_reduction(groove_dia, oring_id):
    oring_stretch_percentage = oring_stretch(groove_dia, oring_id)
    
    if oring_stretch_percentage <= 3:
        a = -0.005 + 1.18 * oring_stretch_percentage
        b = -0.19 * oring_stretch_percentage ** 2
        c = -0.001 * oring_stretch_percentage ** 3
        d = 0.008 * oring_stretch_percentage ** 4
        reduction = a + b + c + d
    else:
        reduction = 0.56 + 0.59 * oring_stretch_percentage - 0.0046 * oring_stretch_percentage ** 2
    return reduction


def oring_stretched_cs_dia(oring_cs_dia, groove_dia, oring_id):
    oring_reduction_percentage = oring_cs_dia_reduction(groove_dia, oring_id)
    return oring_cs_dia - (oring_cs_dia * oring_reduction_percentage / 100)


def oring_stretched_csa(oring_cs_dia, groove_dia, oring_id):
    oring_cs_dia_reduced = oring_stretched_cs_dia(oring_cs_dia, groove_dia, oring_id)
    return math.pi * oring_cs_dia_reduced ** 2 / 4 

# ************************* FRICTION RELATED CALCS *********************
def youngs_modulus(hardness):
    a = (1 - 0.5 ** 2) / (2 * 0.395 * 0.025)
    b = (0.549 + (0.07516 * hardness)) / (100 - hardness)
    c = 2.6 - (0.02 * hardness)
    return a * b * c


def contact_length(oring_cs_dia, groove_dia, oring_id, compression):
    oring_cs_dia_reduced = oring_stretched_cs_dia(oring_cs_dia, groove_dia, oring_id)
    length = 2 * math.sqrt(((oring_cs_dia_reduced / 2) ** 2) - ((oring_cs_dia_reduced/2) - ((oring_cs_dia_reduced * compression) / 200))** 2)
    return length


def contact_area(oring_cs_dia, groove_dia, oring_id, bore_dia, compression):
    contact_len = contact_length(oring_cs_dia, groove_dia, oring_id, compression)
    
    return math.pi * contact_len * bore_dia
    

def contact_stress(hardness, compression):
    youngs = youngs_modulus(hardness)

    return youngs * compression / 100
 

def reaction_force(hardness, groove_dia, oring_id, oring_cs_dia, bore_dia, compression):
    stress = contact_stress(hardness, compression)
    area = contact_area(oring_cs_dia, groove_dia, oring_id, bore_dia, compression)
    
    return stress * area


def friction_force(hardness, bore_dia, groove_dia, oring_id, oring_cs_dia, compression, coef_of_friction):
    reaction = reaction_force(hardness, groove_dia, oring_id, oring_cs_dia, bore_dia, compression)
    return reaction * coef_of_friction


def total_friction_force_range(bore_dia, bore_dia_tol, groove_dia, groove_dia_tol, oring_size, hardness, coef_of_friction):
    
    bore_dia_max, bore_dia_min = dimension_limits(bore_dia, bore_dia_tol)
    groove_dia_max, groove_dia_min = dimension_limits(groove_dia, groove_dia_tol)
        
    comp = total_compression_range(bore_dia, bore_dia_tol, groove_dia, groove_dia_tol, oring_size)
    max_comp = comp['max_comp']
    min_comp = comp['min_comp']
    
    oring_cs_dia_max, oring_cs_dia_min, oring_id_max, oring_id_min = oring_dims(oring_size)
    
    max_friction_force = friction_force(hardness, bore_dia_min, groove_dia_max, oring_id_max, oring_cs_dia_max, max_comp, coef_of_friction)
    min_friction_force = friction_force(hardness, bore_dia_max, groove_dia_min, oring_id_min, oring_cs_dia_min, min_comp, coef_of_friction)
    
    return {"max_friction_force": max_friction_force, "min_friction_force": min_friction_force}

# print(total_compression_range(73.055, 0.025, 63.58, 0.03, 333))
# print(total_gland_fill_range(73.055, 0.025, 63.58, 0.03,6, 0.12, 333))
# print(total_friction_force_range(73.055, 0.025, 63.58, 0.03, 333, 70, 0.4))

print(oring_dims(333))