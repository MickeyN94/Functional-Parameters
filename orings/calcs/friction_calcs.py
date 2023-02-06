from orings.calcs.oring_size_calc import dimension_limits, oring_dims, oring_stretched_cs_dia
from orings.calcs.compression_calc import total_compression_range
import math


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


def friction_force(hardness, bore_dia, groove_dia, oring_id, oring_cs_dia, compression, coef_of_friction):
    reaction = reaction_force(hardness, groove_dia, oring_id, oring_cs_dia, bore_dia, compression)
    return max(reaction * coef_of_friction, 0)


def reaction_force(hardness, groove_dia, oring_id, oring_cs_dia, bore_dia, compression):
    stress = contact_stress(hardness, compression)
    area = contact_area(oring_cs_dia, groove_dia, oring_id, bore_dia, compression)
    
    return stress * area


def contact_stress(hardness, compression):
    youngs = youngs_modulus(hardness)

    return youngs * compression / 100


def contact_area(oring_cs_dia, groove_dia, oring_id, bore_dia, compression):
    contact_len = contact_length(oring_cs_dia, groove_dia, oring_id, compression)
    
    return math.pi * contact_len * bore_dia


def contact_length(oring_cs_dia, groove_dia, oring_id, compression):
    oring_cs_dia_reduced = oring_stretched_cs_dia(oring_cs_dia, groove_dia, oring_id)
    length = 2 * math.sqrt(((oring_cs_dia_reduced / 2) ** 2) - ((oring_cs_dia_reduced/2) - ((oring_cs_dia_reduced * compression) / 200))** 2)
    return length


def youngs_modulus(hardness):
    a = (1 - 0.5 ** 2) / (2 * 0.395 * 0.025)
    b = (0.549 + (0.07516 * hardness)) / (100 - hardness)
    c = 2.6 - (0.02 * hardness)
    return a * b * c





 







