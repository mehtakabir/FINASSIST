from openai import OpenAI
import os
import json

client = OpenAI(api_key="Your_key")

input_folder = "compressed_audios"
output_folder = "jsons"
os.makedirs(output_folder, exist_ok=True)

audios = os.listdir(input_folder)

for audio in audios:
    if "_" in audio and audio.endswith((".mp3", ".wav", ".m4a")):
        number = audio.split("_")[0]
        title = audio.split("_")[1].rsplit(".", 1)[0]  # Better way to remove extension
        print(f"Processing: {number} | {title}")

        audio_path = os.path.join(input_folder, audio)
        
        try:
            with open(audio_path, "rb") as audio_file:
                result = client.audio.translations.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json"
                )

            # Save chunks with timestamps
            chunks = []
            for segment in result.segments:
                chunks.append({
                    "number": number,
                    "title": title,
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text
                })

            # Save with both chunks and full text
            output_data = {
                "chunks": chunks,
                "text": result.text  # Full transcription
            }

            output_path = os.path.join(output_folder, f"{number}_{title}.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

            print(f" Saved: {output_path}")
            
        except Exception as e:
            print(f"Error processing {audio}: {e}")
            continue

print("All files processed and saved in 'jsons' folder")