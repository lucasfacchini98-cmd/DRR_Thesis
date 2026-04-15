import os
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import imageio
import cv2


# === CONFIGURAÇÕES ===
tif_folder = r"/Users/lucasfacchini/Desktop/thesis-project/data/output/Output_folder_tif"
output_folder = "/Users/lucasfacchini/Desktop/thesis-project/data/output/Delta"

# Pastas de saída
frames_dir = "/Users/lucasfacchini/Desktop/thesis-project/data/output/frames"
videos_dir = "/Users/lucasfacchini/Desktop/thesis-project/data/output/videos"

os.makedirs(frames_dir, exist_ok=True)
os.makedirs(videos_dir, exist_ok=True)

# Caminhos dos shapefiles
shapefile_estado = "/Users/lucasfacchini/Desktop/thesis-project/data/shapefiles/RS_UF_2022/RS_UF_2022.shp"
shapefile_municipios = "/Users/lucasfacchini/Desktop/thesis-project/data/shapefiles/RS_Municipios_2022/RS_Municipios_2022.shp"

# Carregar shapefiles
rs_estado = gpd.read_file(shapefile_estado)
rs_municipios = gpd.read_file(shapefile_municipios)

# Áreas de interesse
areas = {
    "Estado": ["Rio Grande do Sul"],
    "Municipios": ["Porto Alegre", "Canoas", "Caxias do Sul", "Pelotas"]
}

# Normalização
lower_bound, upper_bound = 0, 110

# Lista de arquivos .tif
tif_files = sorted([os.path.join(tif_folder, f) for f in os.listdir(tif_folder) if f.endswith(".tif")])

# === LOOP PRINCIPAL ===
for category, names in areas.items():
    for name in names:
        print(f"[PROCESSANDO] {name}...")

        # Criar subpastas para frames e vídeos
        area_frame_dir = os.path.join(frames_dir, category, name.replace(" ", "_"))
        area_video_dir = os.path.join(videos_dir, category, name.replace(" ", "_"))
        os.makedirs(area_frame_dir, exist_ok=True)
        os.makedirs(area_video_dir, exist_ok=True)

        # Preparar vídeo
        video_path = os.path.join(area_video_dir, f"Brightness_Variation_{name.replace(' ', '_')}.mp4")
        out_video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 2, (800, 600))

        # Loop pelos arquivos .tif
        for i, tif_file in enumerate(tif_files):
            with rasterio.open(tif_file) as src:
                # Selecionar geometria
                if category == "Estado":
                    shape = rs_estado[rs_estado['NM_UF'] == name]
                else:
                    shape = rs_municipios[rs_municipios['NM_MUN'] == name]

                if shape.empty:
                    continue

                shapes = [shape.geometry.union_all()]
                out_image, _ = mask(src, shapes, crop=True)

                # Normalizar
                out_image = np.clip(out_image[0], lower_bound, upper_bound)
                out_image = ((out_image - lower_bound) / (upper_bound - lower_bound) * 255).astype(np.uint8)

                # Plotar frame
                plt.figure(figsize=(10, 6))
                plt.imshow(out_image, cmap='inferno', vmin=0, vmax=255)
                plt.title(f"Nightlights - {name} - {os.path.basename(tif_file)}")
                plt.colorbar()

                frame_path = os.path.join(area_frame_dir, f"frame_{i}.png")
                plt.savefig(frame_path, dpi=150)
                plt.close()

                # Adicionar frame ao vídeo
                frame = cv2.imread(frame_path)
                out_video.write(cv2.resize(frame, (800, 600)))

        # Finalizar vídeo
        out_video.release()
        print(f"[SUCESSO] Vídeo salvo em: {video_path}")