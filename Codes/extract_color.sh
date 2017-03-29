for i in `seq 1 192`
do
    # Extract the polygon
    ogr2ogr -f "ESRI Shapefile" /tmp/temp.shp -where "ID = ${i}" ../Data/all_prairies_indices_emp_auch.shp

    # Warp the aperçu
    gdalwarp -cutline /tmp/temp.shp -crop_to_cutline -dstalpha /mnt/Data_1/MUESLI/VNIR_SWIR_2m/L1c/apercu/ENVI/MUESLI_mos_VNIR_SWIR_268_208_123_ENVI Figures/color_${i}.tif
    
    # Clean data
    rm /tmp/temp.*
done
