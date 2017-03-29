# Compute the NDVI
otbcli_BandMath -il /mnt/Data_1/MUESLI/VNIR_SWIR_2m/L1c/atm/mosaic.tif -out /mnt/Data_1/MUESLI/VNIR_SWIR_2m/L1c/atm/ndvi.tif
		    -exp "(im1b107-im1b71)/(im1b107+im1b71)" -ram 4096

for i in `seq 1 192`
do
    # Extract the polygon
    ogr2ogr -f "ESRI Shapefile" /tmp/temp.shp -where "ID = ${i}" ../Data/all_prairies_indices_emp_auch.shp

    # Warp the aperçu
    gdalwarp -cutline /tmp/temp.shp -crop_to_cutline -dstalpha /mnt/Data_1/MUESLI/VNIR_SWIR_2m/L1c/atm/ndvi.tif ../Figures/color_${i}.tif

    # Stretch data
    gdal_translate -scale 0 1 0 255 -of PNG ../Figures/color_${i}.tif ../Figures/color_${i}.png
    
    # Clean data
    rm /tmp/temp.*
done
