import scipy as sp
import sqlite3
from osgeo import gdal, ogr, gdalconst

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

def readSamplesId(DB,ID,bands):
    """
    """
    
    # Create a SQL connection - No check if the DB exists !
    con = sqlite3.connect(DB) 
    cursor = con.cursor()

    # Load samples
    X = []
    for row in cursor.execute("SELECT {} FROM output WHERE id=?".format(bands),(str(ID),)):
        tp = sp.asarray(row).astype(float)
        if not sp.isnan(tp).any() and tp[0] > 0: # Check for nan values
                X.append(tp)
    X = sp.asarray(X)
    return X

    # Close connection
    conn.close()

def readSamples(DB,bands,Field="Class",NODATA=0):
    """
    TBC
    """
    # Initialization
    X,Y,P=[],[],[]

    # Use gdal Exceptions
    gdal.UseExceptions()

    # Open DB with OGR
    driverOgr = ogr.GetDriverByName('SQLite')
    vectorIn = driverOgr.Open(DB,gdalconst.GA_ReadOnly)
    layerIn = vectorIn.GetLayer()

    # # Open raster with GDAL
    # rasterIn = gdal.Open(raster,gdalconst.GA_ReadOnly)
    # if rasterIn is None:
    #     print 'Impossible to open '+filename
    #     exit()

    # W,H,D= rasterIn.RasterXSize,rasterIn.RasterYSize,rasterIn.RasterCount
    # GeoTransform = rasterIn.GetGeoTransform()
    # Projection = rasterIn.GetProjection()
    # ox,oy = GeoTransform[0],GeoTransform[3]
    # sx,sy = GeoTransform[1],GeoTransform[5]

    # print "X={},Y={},D={}".format(W,H,D)
    
    # Iterate over features and store pixels position
    for feat in layerIn:
        geom = feat.GetGeometryRef()
        if feat.GetField("band_0") != NODATA:
            P.append([geom.GetX(),geom.GetY()])
            Y.append(feat.GetField(Field))
            X.append([feat.GetField(b) for b in bands])
            
        # pi_ = [sp.floor((Xc-ox)/sx).astype(int), sp.floor((Yc-oy)/sy).astype(int)]
        # if (pi_[0]>=0) and (pi_[0]<W) and (pi_[1]>=0) and (pi_[1]<H): # Check if the point is in the image
        #     pi.append(pi_)
        #     y.append(feat.GetField(Field))  
        

    # # Filter NODATA values
    # band = rasterIn.GetRasterBand(1).ReadAsArray()
    # PI,Y=[],[]
    # for y_,pi_ in zip(y,pi):x
    #     if band[pi_[1], pi_[0]] > 0:
    #         PI.append(pi_)
    #         Y.append(y_)
    # del y,pi
    
    # # Load samples
    # ns = len(Y)
    # X = sp.empty((ns,bands.size))
    # print X.shape
    # for d_ in bands:
    #     print "Bands number {}".format(d_)
    #     band = rasterIn.GetRasterBand(d_+1).ReadAsArray()
    #     for p, pi_ in enumerate(PI):
    #         X[p, d_] = band[pi_[1], pi_[0]]

    return X,Y,P
