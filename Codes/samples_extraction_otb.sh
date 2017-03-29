# Class statistics
FIELD='id'
otbcli_PolygonClassStatistics -in /mnt/Data_1/MUESLI/VNIR_SWIR_2m/L1c/atm/mosaic.tif \
			      -vec all_prairies_indices_emp_auch.shp \
			      -out classStat_${FIELD}.xml \
			      -field ${FIELD}

# Samples selection
otbcli_SampleSelection -in /mnt/Data_1/MUESLI/VNIR_SWIR_2m/L1c/atm/mosaic.tif \
		       -vec all_prairies_indices_emp_auch.shp \
		       -out samplesSelected_${FIELD}.sqlite \
		       -instats classStat_${FIELD}.xml \
		       -field ${FIELD} \
		       -strategy all  -ram 8192

# Samples Extraction
otbcli_SampleExtraction -in /mnt/Data_1/MUESLI/VNIR_SWIR_2m/L1c/atm/mosaic.tif \
			 -vec samplesSelected_${FIELD}.sqlite \
			 -out prairie_${FIELD}.sqlite \
			 -outfield prefix \
			 -outfield.prefix.name band_ \
			 -field ${FIELD} -ram 8192
