from orings.calcs.oring_size_calc import dimension_limits, oring_dims, oring_stretched_cs_dia

def total_compression_range(bore_dia, bore_dia_tol, groove_dia, groove_dia_tol, oring_size):

    bore_dia_max, bore_dia_min = dimension_limits(bore_dia, bore_dia_tol)
    groove_dia_max, groove_dia_min = dimension_limits(groove_dia, groove_dia_tol)

    oring_cs_dia_max, oring_cs_dia_min, oring_id_max, oring_id_min = oring_dims(oring_size)

    max_comp = compression(groove_dia_max, oring_id_max, oring_cs_dia_max, bore_dia_min)
    min_comp = compression(groove_dia_min, oring_id_min, oring_cs_dia_min, bore_dia_max)

    return {"max_comp": max_comp, "min_comp": min_comp}


def compression(groove_dia, oring_id, oring_cs_dia, bore_dia):
    
    oring_cs_dia_reduced = oring_stretched_cs_dia(oring_cs_dia, groove_dia, oring_id)
    return max((oring_cs_dia_reduced - ((bore_dia - groove_dia)/2))/oring_cs_dia_reduced * 100, 0)