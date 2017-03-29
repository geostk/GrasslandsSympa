for i in `seq 1 192`
do
    # Extract the polygon
    ogr2ogr -f "ESRI Shapefile" /tmp/temp.shp -where "ID = ${i}" ../Data/all_prairies_indices_emp_auch.shp

    # Warp the aperçu
    gdalwarp -cutline /tmp/temp.shp -crop_to_cutline /mnt/Data_1/MUESLI/VNIR_SWIR_2m/L1c/atm/mosaic.tif /tmp/temp.tif

    # Compute the NDVI
    otbcli_BandMath -il /tmp/temp.tif -out /tmp/ndvi.tif -exp "(im1b107-im1b71)/(im1b107+im1b71)" -ram 4096

    # Stretch data
    gdal_translate -scale 0 1 0 255 -of PNG /tmp/ndvi.tif ../Figures/color_${i}.png
    
    # Clean data
    rm /tmp/temp.* /tmp/ndvi.tif
done
