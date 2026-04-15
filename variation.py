import numpy as np
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import imageio

def crop_and_mask(tiff, shapes):
    out_image, out_transform = mask(tiff, shapes, crop=True)
    return out_image[0]

# Caminhos dos shapefiles
shapefile_path_municipios = "/Users/lucasfacchini/Desktop/thesis-project/data/shapefiles/RS_Municipios_2022/RS_Municipios_2022.shp"
shapefile_path_estado = "/Users/lucasfacchini/Desktop/thesis-project/data/shapefiles/RS_UF_2022/RS_UF_2022.shp"

rs_municipios = gpd.read_file(shapefile_path_municipios)
rs_estado = gpd.read_file(shapefile_path_estado)

# Áreas desejadas
areas = ["Rio Grande do Sul", "Porto Alegre", "Canoas", "Caxias do Sul"]

lon_min, lon_max = -60.0, -40.0
lat_min, lat_max = -40.0, -20.0

output_dir = "data/output/Delta"
os.makedirs(output_dir, exist_ok=True)

for area in areas:
    if area == "Rio Grande do Sul":
        area_shape = rs_estado
    else:
        area_shape = rs_municipios[rs_municipios['NM_MUN'] == area]

    if area_shape.empty:
        print(f"[AVISO] Nenhum polígono encontrado para {area}")
        continue

    shapes = [area_shape.geometry.unary_union]

    # Lista de frames para esta área
    area_images = []

    # Loop de diferenças consecutivas
    for day in range(101, 130):
        prev_day = day - 1

        tiff_day_prev_path = f"/Users/lucasfacchini/Desktop/thesis-project/data/output/Output_folder_tif/output_day_{prev_day}.tif"
        tiff_day_curr_path = f"/Users/lucasfacchini/Desktop/thesis-project/data/output/Output_folder_tif/output_day_{day}.tif"

        if not os.path.exists(tiff_day_prev_path) or not os.path.exists(tiff_day_curr_path):
            print(f"[AVISO] Arquivos ausentes para dia {day} vs {prev_day}")
            continue

        with rasterio.open(tiff_day_prev_path) as src_prev:
            crop_prev = crop_and_mask(src_prev, shapes)

        with rasterio.open(tiff_day_curr_path) as src_curr:
            crop_curr = crop_and_mask(src_curr, shapes)

        crop_prev[crop_prev > 100] = 100
        crop_curr[crop_curr > 100] = 100

        delta = crop_curr - crop_prev

        # Plotar e salvar cada frame
        plt.figure(figsize=(10, 8))
        plt.imshow(delta, cmap='plasma', extent=(lon_min, lon_max, lat_min, lat_max), vmin=0, vmax=100)
        plt.colorbar(label='Brightness Variation')
        plt.title(f"Brightness Delta: Day {day} vs Day {prev_day} - {area}")
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

        frame_path = os.path.join(output_dir, f"Delta_{area.replace(' ', '_')}_day{day}_vs_day{prev_day}.png")
        plt.savefig(frame_path, dpi=300)
        plt.close()

        if os.path.exists(frame_path):
            area_images.append(imageio.imread(frame_path))

    # Criar GIF para esta área
    if area_images:
        gif_path = os.path.join(output_dir, f"Brightness_Variation_{area.replace(' ', '_')}.gif")
        imageio.mimsave(gif_path, area_images, fps=2)
        print(f"[SUCESSO] GIF criado: {gif_path}")
    else:
        print(f"[ERRO] Nenhum frame encontrado para {area}, GIF não criado.")
