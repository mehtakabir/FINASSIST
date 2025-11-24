import os
import subprocess

input_folder = "audios"
output_folder = "compressed_audios"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".mp3"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        subprocess.run([
            "ffmpeg", "-i", input_path, "-b:a", "64k", output_path, "-y"
        ])
print("Compression complete Saved in 'compressed_audios' folder.")

