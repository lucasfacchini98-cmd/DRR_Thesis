import os
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np

# Path to the folder containing .tif files
tif_folder = r"/Users/lucasfacchini/Desktop/thesis-project/data/output/Output_folder_tif"
output_folder = r"/Users/lucasfacchini/Desktop/thesis-project/data/output/cropped_Riogrande"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load the shapefile for Rio Grande do Sul (or the area of interest)
shapefile_path = r"data/shapefiles/RS_UF_2022/RS_UF_2022.shp"
gdf = gpd.read_file(shapefile_path)

# Normalize the raster values
lower_bound = 0
upper_bound = 110  # Adjust this value depending on the analysis

for tif_file in os.listdir(tif_folder):
    if tif_file.endswith(".tif"):
        tif_path = os.path.join(tif_folder, tif_file)

        with rasterio.open(tif_path) as src:
            # Crop the raster using the shapefile
            out_image, out_transform = mask(src, gdf.geometry, crop=True)
            out_meta = src.meta.copy()

            # Normalize the values
            clipped_data_normalized = np.clip(out_image, lower_bound, upper_bound)
            clipped_data_normalized = ((clipped_data_normalized - lower_bound) / (upper_bound - lower_bound) * 255).astype(np.uint8)

            # Update the metadata
            out_meta.update({
                "driver": "GTiff",
                "dtype": 'uint8',  # Change the data type to uint8 for normalization
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform
            })

            # Save the normalized and cropped raster
            output_tif_path = os.path.join(output_folder, f"normalized_clipped_{tif_file}")
            with rasterio.open(output_tif_path, "w", **out_meta) as dest:
                dest.write(clipped_data_normalized)

        print(f"File {tif_file} cropped, normalized, and saved to {output_tif_path}")


        