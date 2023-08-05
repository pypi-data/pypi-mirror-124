import numpy as np
import pandas as pd
from pathlib import Path

def unit2unit(val, choice):
    """
    Input:
    ------
    val:
        value of which the unit to be changed. 
    choice: int
        what unit change to what unit?
        g/kg -> kg/kg
    """
    if (choice == "g/kg -> kg/kg") or (choice == 1):
        val = val / 1000
    elif (choice == "g/m3 -> mg/m3") or (choice == 2):
        val = val * 1000
    else:
        raise(Exception("Must specify a correct choice"))
    return val

def fetch_sort_path(root_proj = None, inputlist = None, return_time = True):
    if root_proj:
        paths = root_proj.glob("*.dat")
        paths = list(paths)
    elif inputlist:   
        with open(inputlist, 'r') as f:
            paths = f.readlines()
        paths = [Path(p.strip()) for p in paths]
    else:
        raise Exception('No input list or data directory!')
    # --------------------------------------------------------------------------------------------------
    path_time = [pd.to_datetime("".join(p.stem.split("_")[-4::]), format = "%Y%m%d%H%M") for p in paths]
    paths = [p for _, p in sorted(zip(path_time, paths))]
    path_time = sorted(path_time)
    # print(path_time)
    if return_time:
        return paths, path_time
    else:
        return paths
    
def group_day(paths, path_time):
    groups = pd.DataFrame(
        zip([p.year for p in path_time], [p.month for p in path_time], [p.day for p in path_time], paths), 
        columns = ['year', 'month', 'day', 'path']
    ).groupby(['year', 'month', 'day'])
    
    return groups