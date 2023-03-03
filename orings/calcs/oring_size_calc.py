import math
import csv
import os
def dimension_limits(dimension, tolerance):
    return dimension + tolerance, dimension - tolerance


def oring_dims(oring):
    
    # if oring[0] true then BS1806 tick box checked so searches oring_size.csv to find dims related to the BS1806 value
    if oring[0]:
        oring_id, oring_cs_dia, oring_id_tol, o_ring_cs_dia_tol = bs1806_oring(oring[1])
        
    else:
        _, _, oring_id, oring_cs_dia, oring_id_tol, o_ring_cs_dia_tol = oring
        
    oring_cs_dia_max, oring_cs_dia_min = dimension_limits(oring_cs_dia, o_ring_cs_dia_tol)
    oring_id_max, oring_id_min = dimension_limits(oring_id, oring_id_tol)
    
    
    return oring_cs_dia_max, oring_cs_dia_min, oring_id_max, oring_id_min


def bs1806_oring(oring_size):
    cwd = os.getcwd()
    with open(f'{cwd}\orings\calcs\data\o-ring_sizes.csv') as csvfile:
        reader = csv.reader(csvfile)

        # check that the oring size given is in BS1806
        sizes = [row[0] for row in reader]
        if oring_size in sizes:
            # find the row that the oring size matches with from BS1806
            csvfile.seek(0)
            for row in reader:
                if row[0] == oring_size:

                    # convert all values from string to floats to return
                    dims = [float(val) for val in row]
                    return dims[1:]
        else:
            print(f"O-ring size not in BS1806: {oring_size}")


def total_oring_stretch_range(groove_dia, groove_dia_tol, oring):
    _, _, oring_id_max, oring_id_min = oring_dims(oring)
    groove_dia_max, groove_dia_min = dimension_limits(groove_dia, groove_dia_tol)
    
    
    max_stretch = oring_stretch(groove_dia_max, oring_id_min)    
    min_stretch = oring_stretch(groove_dia_min, oring_id_max)
    
    return {"max_stretch": max_stretch, "min_stretch": min_stretch}    


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

