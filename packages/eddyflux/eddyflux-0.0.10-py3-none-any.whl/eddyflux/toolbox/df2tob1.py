import struct
import numpy as np
import pandas as pd
from copy import deepcopy

def int2little(val):
    little_hex = struct.pack('I', val)
    # str_little = ''.join(format(x, '02x') for x in little_hex)
    # return str_little.upper()
    return little_hex

def FP22big(val):
    # big_hex = hex(val).replace('0x', '\\x')
    big_hex = struct.pack('>H', val)
    # # or:
    # str_big = big_hex[2::]
    # return str_big.upper()
    # return big_hex.encode('utf-8')
    return big_hex

def val2FP2(val):
    '''
    FP2:
    A two-byte floating-point number format created by Campbell Scientific, Inc.and used to store low-resolution values. 
    Appendix C of the CR10X dataloggermanual describes this format in greater detail. 
    Basically, this format consists ofa single sign bit, a two-bit negative decimal exponent, and a 13-bit mantissa.
    
    FP2 decimal location
    -----------------------------------
    |Absolute value | Decimal location|
    |0 – 7.999      | X.XXX           |
    |8 – 79.99      | XX.XX           |
    |80 – 799.9     | XXX.X           |
    |800 – 7999.    | XXXX.           |
    -----------------------------------
    Ref:
    [1] https://numpy.org/doc/stable/user/basics.types.html
    [2] https://help.campbellsci.com/CR6/Content/shared/Details/Data/data-types-storage.htm?TocPath=Data%20storage%7C_____0
    '''
    if np.isnan(val):
        return 0x9ffe
    elif np.isinf(val):
        if val > 0:
            return 0x1fff
        else:
            return 0x9fff
    elif val == 0.:
        return 0x6000
    else:
        if val < 0:

            isNeg = 0x8000
        else:
            isNeg = 0x0
        val = np.abs(val)
        if (val > 0) & (np.round(val, 3) <= 8.000): # (0 - 7.999)
            expnt = 3
        elif (val > 8) & (np.round(val, 2) <= 80.00): # (8 - 79.99)
            expnt = 2
        elif (val > 80) & (np.round(val, 1) <= 800.0): # (80 - 799.9)
            expnt = 1
        elif (val > 800) & (np.round(val) <= 8000.): # (800 - 7999.)
            expnt = 0
        else:
            raise Exception(f'{val} exceeding FP2 limit 7999.')
        # expnt = 4 - len(str(val).split(".")[0])
        # expnt = len(str(0x1fff / val).split(".")[0]) - 1
        # while expnt > 3: expnt = expnt - 1
        mantis = int(np.round(val * 10**expnt))
        return mantis | (expnt << 13) | isNeg

def dataframe2tob1(df, p_header, p_save, nlines = 5, lname = 1, lunit = 2, ldtype = 4):
    '''
    Header structure, 
    nlines: header lines
    lname: variable name line
    lunit: variable unit line
    ldtype: variable datatype line
    '''
    df = df.copy()

    TYPE_MAP = {
        "IEEE4": np.float32,
        "IEEE8": np.float64,
        "LONG": np.int32,
        "ULONG": np.uint32,
        "FP2": np.dtype('>H'),  # big-endian unsigned short
    }

    with open(p_header, "rb") as f:
        headers = []
        for l in range(nlines):
            headers.append(f.readline())
        names = headers[lname].decode().strip().replace('"', "").split(",")
        if lunit:
            units = headers[lunit].decode().strip().replace('"', "").split(",")
        types = headers[ldtype].decode().strip().replace('"', "").split(",")
        dtype = np.dtype([(n, TYPE_MAP[t]) for n, t in zip(names, types)])
    
    big2little_names = pd.Index(deepcopy(names))
    if "FP2" in types:
        fp2_df = pd.DataFrame(zip(names, types), columns = ["name", "type"])
        fp2_names = fp2_df.loc[fp2_df["type"] == "FP2", "name"].tolist()
        # --------------------------------------------------------------------------------
        fp2vals = df[fp2_names].values
        if len(fp2vals[np.where(fp2vals > 9999.)]) > 0: raise Exception('Too large value!')
        # ----------------------------------------------------------------------------
        df.loc[:, fp2_names] = df.loc[:, fp2_names].applymap(val2FP2).applymap(FP22big)
        big2little_names = big2little_names.difference(fp2_names)
    df.loc[:, big2little_names] = df.loc[:, big2little_names].applymap(int2little)

    # ========================================================================================
    # write to file
    hex_headers = b"".join(headers)

    hex_body = []
    for cnt, row in df.iterrows():
        row = b"".join(row.to_list())
        hex_body.append(row)
    hex_body = b"".join(hex_body)
    hex_text = hex_headers + hex_body

    with open(p_save, "wb") as f:
        f.write(hex_text)
