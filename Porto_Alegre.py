import os
import rasterio
import matplotlib.pyplot as plt
import geopandas as gpd
from rasterio.mask import mask
import cv2

# Folder containing all cropped .tif files
tif_folder = r"/Users/lucasfacchini/Desktop/thesis-project/data/output/cropped_Riogrande"
tif_files = sorted([os.path.join(tif_folder, f) for f in os.listdir(tif_folder) if f.endswith('.tif')])

# Shapefile path
shapefile_path = r"/Users/lucasfacchini/Desktop/thesis-project/data/shapefiles/RS_Municipios_2022"
gdf = gpd.read_file(shapefile_path)

# Select city of interest
municipality = 'Porto Alegre'
gdf_selected = gdf[gdf['NM_MUN'] == municipality]

# Prepare video writer (output file, codec, frame size)
output_video_path = r"/Users/lucasfacchini/Desktop/thesis-project/data/video/nightlights_porto_alegre.mp4"
out_video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (800, 600))

# Loop through each TIFF file (day by day for Porto Alegre)
for tif_file in tif_files:
    with rasterio.open(tif_file) as src:
        # Crop the raster to the municipality area
        out_image, out_transform = mask(src, gdf_selected.geometry, crop=True)

        # Plot the nightlights for Porto Alegre
        plt.figure(figsize=(10, 6))
        plt.imshow(out_image[0], cmap='inferno', vmin=0, vmax=255)
        plt.title(f'Nightlights for Porto Alegre - {tif_file[-14:-4]}')
        plt.colorbar()
        plt.savefig('temp_frame.png')
        plt.close()

        # Add frame to the video
        frame = cv2.imread('temp_frame.png')
        out_video.write(cv2.resize(frame, (800, 600)))

# Release video writer
out_video.release()
print(f"Video showing daily nightlights saved at: {output_video_path}")