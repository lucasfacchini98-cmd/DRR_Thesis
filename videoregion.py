import os
import rasterio
import matplotlib.pyplot as plt
import cv2

# Folder containing all cropped .tif files
tif_folder = r"/Users/lucasfacchini/Desktop/thesis-project/data/output/cropped_Riogrande"
tif_files = sorted([os.path.join(tif_folder, f) for f in os.listdir(tif_folder) if f.endswith('.tif')])

# Output video path
output_video_path = r"/Users/lucasfacchini/Desktop/thesis-project/data/video/nightlights_region.mp4"
os.makedirs(os.path.dirname(output_video_path), exist_ok=True)

# Define frame size (width, height)
frame_size = (800, 600)

# Prepare video writer
fourcc = cv2.VideoWriter_fourcc(*'avc1')  # try 'mp4v' if 'avc1' fails
out_video = cv2.VideoWriter(output_video_path, fourcc, 2, frame_size)

for tif_file in tif_files:
    with rasterio.open(tif_file) as src:
        plt.figure(figsize=(8, 6), dpi=100)  # ensures 800x600 output
        plt.imshow(src.read(1), cmap='inferno', vmin=0, vmax=255)
        plt.title(f'Nightlights for Rio Grande do Sul - {tif_file[-14:-4]}')
        plt.colorbar()
        plt.savefig('temp_frame.png', bbox_inches='tight')
        plt.close()

        frame = cv2.imread('temp_frame.png')
        if frame is None:
            print(f"Could not read frame for {tif_file}")
            continue

        frame = cv2.resize(frame, frame_size)
        out_video.write(frame)

out_video.release()
print(f"Video saved at: {output_video_path}")
