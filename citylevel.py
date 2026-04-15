import rasterio 
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from rasterio.mask import mask

# Paths to the two .tif files
tif_file_1 = r"/Users/lucasfacchini/Desktop/thesis-project/data/output/cropped_Riogrande/normalized_clipped_output_day_100.tif"
tif_file_2 = r"/Users/lucasfacchini/Desktop/thesis-project/data/output/cropped_Riogrande/normalized_clipped_output_day_129.tif"
# Load the shapefile to get the geometries of the municipalities
shapefile_path = r"/Users/lucasfacchini/Desktop/thesis-project/data/shapefiles/RS_Municipios_2022/RS_Municipios_2022.shp"
gdf = gpd.read_file(shapefile_path)

# Select multiple municipalities based on the "NAME_2" field
municipalities_to_select = ['Pelotas', 'Porto Alegre', 'Canoas', 'Caxias do Sul']
gdf_selected = gdf[gdf['NM_MUN'].isin(municipalities_to_select)]

# Load the two rasters
with rasterio.open(tif_file_1) as src1, rasterio.open(tif_file_2) as src2:
    # Loop for each selected municipality
    for city in municipalities_to_select:
        city_gdf = gdf_selected[gdf_selected['NM_MUN'] == city]

        # Crop the rasters for each city
        out_image_1, out_transform_1 = mask(src1, city_gdf.geometry, crop=True)
        out_image_2, out_transform_2 = mask(src2, city_gdf.geometry, crop=True)

        # Display the nightlights for the first day
        plt.figure(figsize=(10, 6))
        plt.imshow(out_image_1[0], cmap='inferno', vmin=0, vmax=255)
        plt.colorbar()
        plt.title(f'Nightlights - April 2 - {city}')
        plt.show()

        # Display the nightlights for the second day
        plt.figure(figsize=(10, 6))
        plt.imshow(out_image_2[0], cmap='inferno', vmin=0, vmax=255)
        plt.colorbar()
        plt.title(f'Nightlights - May 14 - {city}')
        plt.show()

        # Calculate the difference between the two rasters
        difference = out_image_1[0] - out_image_2[0]

        # Display the difference between the two days for the current city
        plt.figure(figsize=(10, 6))
        plt.imshow(difference, cmap='inferno', vmin=0, vmax=250)
        plt.colorbar()
        plt.title(f'Difference in nightlights for {city}')
        plt.show()

print("Visualization complete")