from orings.calcs.oring_size_calc import dimension_limits, oring_dims, oring_stretched_csa


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