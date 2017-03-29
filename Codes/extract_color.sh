from osgeo import ogr,gdalconst

# Data name
inVector = "Data/all_prairies_indices_emp_auch.shp"
driver = ogr.GetDriverByName('ESRI Shapefile')

# Open data
vectorIn = driver.Open(inVector, gdalconst.GA_ReadOnly)
layerIn = vectorIn.GetLayer()

print layerIn.GetFeatureCount()
