import rasterio
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from rasterio.mask import mask

# Paths to the two .tif files
tif_file_1 = r"/Users/lucasfacchini/Desktop/thesis-project/data/output/cropped_Riogrande/normalized_clipped_output_day_100.tif"
tif_file_2 = r"/Users/lucasfacchini/Desktop/thesis-project/data/output/cropped_Riogrande/normalized_clipped_output_day_129.tif"

# Load the shapefile to get the geometries of the municipalities
shapefile_path = r"/Users/lucasfacchini/Desktop/thesis-project/data/shapefiles/RS_UF_2022/RS_UF_2022.shp"
gdf = gpd.read_file(shapefile_path)

# Select the municipality "Porto Alegre" based on the "NAME_2" field
municipalities_to_select = ['Rio Grande do Sul']
gdf_selected = gdf[gdf['NM_UF'].isin(municipalities_to_select)]

# Load the two rasters and crop the area of the selected municipalities
with rasterio.open(tif_file_1) as src1, rasterio.open(tif_file_2) as src2:
    # Crop the rasters using the selected geometries
    out_image_1, out_transform_1 = mask(src1, gdf_selected.geometry, crop=True)
    out_image_2, out_transform_2 = mask(src2, gdf_selected.geometry, crop=True)
    
    # Display the night lights for the first day
    plt.figure(figsize=(10, 6))
    plt.imshow(out_image_1[0], cmap='inferno', vmin=0, vmax=255)
    plt.colorbar()
    plt.title('Night Lights - Apr 2 - Rio Grande do Sul')
    plt.show()
    
    # Display the night lights for the second day
    plt.figure(figsize=(10, 6))
    plt.imshow(out_image_2[0], cmap='inferno', vmin=0, vmax=255)
    plt.colorbar()
    plt.title('Night Lights - May 14 - Rio Grande do Sul')
    plt.show()
    
    # Calculate the difference between the two cropped rasters
    difference = out_image_2[0] - out_image_1[0]

# Display the difference between the two days with a warm colormap (e.g., inferno)
plt.figure(figsize=(10, 6))
plt.imshow(difference, cmap='plasma', vmin=0, vmax=255)  # Adjust vmin and vmax if necessary
plt.colorbar()
plt.title('Light Intensity Difference for Rio Grande do Sul')
plt.show()

print("Visualization complete")