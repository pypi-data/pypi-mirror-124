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
    if np.isnan(val):
        return 0x9ffe
    elif np.isinf(val):
        if val > 0:
            return 0x1fff
        else:
            return 0x9fff
    else:
        if val < 0:

            isNeg = 0x8000
        else:
            isNeg = 0x0
        val = np.abs(val)
        expnt = 4 - len(str(val).split(".")[0])
        mantis = int(val * 10**expnt)

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
