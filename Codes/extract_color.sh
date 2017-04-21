for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 20 21 22 23 24 25 26 27 28 33 35 36 37 38 39 42 43 44 46 47 48 49 50 51 52 53 54 55 56 57 8 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 93 94 95 96 97 98 99 100 103 104 105 106 107 108 109 110 111 113 114 115 116 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 141 143
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
