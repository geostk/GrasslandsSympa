import scipy as sp
import sqlite3

def read2bands(DB,b1,b2):
    """The function  reads two bands  from the database and  group samples
    with the same ID.

    """

    # Create a SQL connection - No check if the DB exists !
    con = sqlite3.connect(DB) 
    cursor = con.cursor()

    # Get the IDs
    id_pp = []
    for row in cursor.execute("SELECT id FROM output WHERE band_0 > 0"): # Read only grasslands that intersect with the MUESLI area
        if row[0] not in id_pp:
            id_pp.append(row[0])

    # Load one grassland per iteration
    X = list()
    for id_ in id_pp:
        # Load variables
        X_ = list()
        for row in cursor.execute("SELECT band_{}, band_{} FROM output WHERE id=?".format(b1,b2),(id_,)):
            tp = sp.asarray(row).astype(float)
            if not sp.isnan(tp).any(): # Check for nan values
                X_.append(tp)
        X.append(sp.asarray(X_))

    return X,id_pp
