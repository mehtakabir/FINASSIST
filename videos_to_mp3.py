import os
import subprocess

# Make sure "audios" folder exists
os.makedirs("audios", exist_ok=True)

files = os.listdir("videos")

for file in files:
    if not file.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".flv")):
        continue
    
    file_name = os.path.splitext(file)[0]
    input_path = os.path.join("videos", file)
    output_path = os.path.join("audios", f"{file_name}.mp3")

    print(f"Converting: {input_path} -> {output_path}")
    subprocess.run([
        "ffmpeg", "-i", input_path, "-q:a", "0", "-map", "a", output_path
    ])
