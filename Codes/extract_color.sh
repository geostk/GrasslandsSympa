WDIR=/media/Data/Data/MUESLI/spectresPrairies
for i in `seq 1 117`
do
    # Extract the polygon
    ogr2ogr -f "ESRI Shapefile" /tmp/temp.shp -where "ID = ${i}" ${WDIR}/Data/all_prairies_indices_emp_auch_intersection.shp

    # Warp the mosaic
    gdalwarp -wm 500 -multi -cutline /tmp/temp.shp -crop_to_cutline /mnt/Data_2/MUESLI/Hyper/muesli_2m.tif /tmp/temp.tif

    # Compute the NDVI
    otbcli_BandMath -il /tmp/temp.tif -out /tmp/ndvi.tif -exp "(im1b107-im1b71)/(im1b107+im1b71)" -ram 4096

    # Stretch NDVI
    gdal_translate -a_nodata 0 -scale 0 1 0 255 -of PNG /tmp/ndvi.tif ${WDIR}/Figures/ndvi_${i}.png 

    # Warp the "apercu"
    gdalwarp -wm 500 -multi -cutline /tmp/temp.shp -crop_to_cutline /mnt/Data_2/MUESLI/Hyper/Apercu/apercu_1m /tmp/temp.tif

    # Stretch NDVI
    gdal_translate -a_nodata 0 -scale -of PNG /tmp/ndvi.tif ${WDIR}/Figures/color_${i}.png
    
    # Clean data
    rm /tmp/temp.* /tmp/ndvi.tif
done
