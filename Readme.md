# RAG-Based Course Teaching Assistant

A command-line RAG (Retrieval Augmented Generation) system that helps students find specific content in course videos by answering questions with precise video references and timestamps.

## Project Overview

This system processes course videos, extracts transcripts, creates embeddings, and provides an intelligent Q&A interface where students can ask questions and get directed to specific video segments.

## Features

- Video to audio conversion
- Audio transcription with timestamps using OpenAI Whisper
- Semantic search using BGE-M3 embeddings via Ollama
- AI-powered responses with GPT-4
- Command-line interface for easy interaction
- Precise video references with timestamps
- Saves responses to text files for review

## Prerequisites

1. Python 3.8 or higher
2. FFmpeg for video/audio processing
3. Ollama installed and running
4. OpenAI API key

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg

For Ubuntu/Debian:
```bash
sudo apt-get install ffmpeg
```

For MacOS:
```bash
brew install ffmpeg
```

For Windows:
Download from https://ffmpeg.org/download.html and add to PATH

### 3. Install and Setup Ollama

Download from https://ollama.com

Pull the BGE-M3 model:
```bash
ollama pull bge-m3
```

Start Ollama server:
```bash
ollama serve
```

Keep this terminal running in the background.

### 4. Configure API Keys

Create a config.py file in the project root:
```python
api_key="your_openai_api_key_here"
```

## Project Structure

```
project/
├── videos/                    # Place your video files here
├── audios/                    # Converted audio files
├── compressed_audios/         # Compressed audio files
├── jsons/                     # Transcript JSON files with timestamps
├── newjsons/                  # Merged chunk JSON files
├── videos_to_mp3.py          # Convert videos to MP3
├── compress.py               # Compress audio files
├── mp3_to_json.mp3.py        # Transcribe audio to JSON
├── merge_chunks.py           # Merge small chunks for better accuracy
├── preprocess_json.py        # Create embeddings
├── process_incoming.py       # Main CLI application
├── config.py                 # Configuration file with API key
├── requirements.txt          # Python dependencies
├── embeddings.joblib         # Generated embeddings file
├── prompt.txt                # Generated prompt for debugging
├── response.txt              # AI generated response
└── README.md                 # This file
```

## Usage

### Step 1: Prepare Your Videos

Place all course video files in the videos/ folder. Supported formats: MP4, MKV, AVI, MOV, FLV

Video files should be named as: `number_title.extension`

Example: `01_Introduction to ML.mp4`

### Step 2: Convert Videos to Audio

```bash
python videos_to_mp3.py
```

This creates MP3 files in the audios/ folder.

### Step 3: Compress Audio Files (Optional but Recommended)

```bash
python compress.py
```

This compresses audio files to 64k bitrate and saves them in compressed_audios/ folder. This is useful if your audio files are larger than 25MB (OpenAI API limit).

### Step 4: Transcribe Audio to JSON

Update your OpenAI API key in mp3_to_json.mp3.py, then run:

```bash
python mp3_to_json.mp3.py
```

This uses OpenAI Whisper API to transcribe audio with timestamps and saves JSON files in jsons/ folder.

### Step 5: Merge Chunks (Recommended)

```bash
python merge_chunks.py
```

This merges every 5 chunks into one for better accuracy and context. Creates files in newjsons/ folder.

### Step 6: Create Embeddings

Make sure Ollama is running, then:

```bash
python preprocess_json.py
```

This creates embeddings.joblib file containing all video chunk embeddings using the BGE-M3 model.

### Step 7: Ask Questions

```bash
python process_incoming.py
```

The program will prompt you to ask a question. Type your question and press Enter. The response will be displayed in the terminal and saved to response.txt file.

## How It Works

1. Videos are converted to audio files using FFmpeg
2. Audio is transcribed using OpenAI Whisper API with timestamps
3. Transcripts are split into chunks with time ranges
4. Small chunks are merged for better context (optional but recommended)
5. Each chunk is converted to embeddings using BGE-M3 model via Ollama
6. User questions are converted to embeddings
7. System finds most similar chunks using cosine similarity
8. Relevant chunks are sent to GPT-4 for natural language response
9. Response includes video numbers and timestamps for easy navigation

## Configuration

### Change Number of Search Results

In process_incoming.py, modify the top_results variable:

```python
top_results = 5  # Change to 3 or 7 based on your needs
```

### Change Compression Quality

In compress.py, modify the bitrate:

```python
"-b:a", "64k"  # Change to 96k or 128k for better quality
```

### Change Chunk Merging Size

In merge_chunks.py, modify the n variable:

```python
n = 5  # Change to 3 or 7 based on your needs
```

### Change AI Model

In process_incoming.py, modify the model in the inference function:

```python
model="gpt-4"  # Change to "gpt-3.5-turbo" or "gpt-4-turbo"
```

## Troubleshooting

### Problem: Embeddings not loading

Solution: Make sure you ran preprocess_json.py and embeddings.joblib file exists in the project root

### Problem: Ollama connection error

Solution: Start Ollama server with `ollama serve` and ensure it is running on port 11434

### Problem: OpenAI API error

Solution: Check that your API key in config.py is valid and has credits

### Problem: FFmpeg not found

Solution: Install FFmpeg and ensure it is in your system PATH

### Problem: Audio files too large

Solution: Run compress.py to compress audio files before transcription

### Problem: Module not found errors

Solution: Install all dependencies with `pip install -r requirements.txt`

### Problem: JSON files not created

Solution: Check that compressed_audios folder has MP3 files and your OpenAI API key is valid

## Running Order

Always start services in this order:

1. Start Ollama: `ollama serve`
2. Process your videos (steps 1-6 above)
3. Run the application: `python process_incoming.py`

## Cost Considerations

- OpenAI Whisper API: Charged per minute of audio transcribed ($0.006 per minute)
- OpenAI GPT-4 API: Charged per token used
- Ollama: Free, runs locally

Estimate costs before processing large amounts of content.

## Limitations

- Ollama must run locally
- Requires decent RAM for embeddings (500MB+ for 100 videos)
- OpenAI API requires internet connection
- Processing time depends on video length
- Command-line interface only

## Security

Never commit config.py or API keys to version control.

Add to .gitignore:
```
config.py
*.joblib
audios/
videos/
compressed_audios/
jsons/
newjsons/
__pycache__/
prompt.txt
response.txt
```

## Example Output

When you ask "where is univariate analysis taught", you might get:

```
Here's where "univariate analysis" is covered in the course:

- Video 8: Machine Learning Development Life Cycle
  - Brief mention/definition around 11:17-11:21 (about 4 seconds total)

- Video 18: EDA using Univariate Analysis
  - Dedicated coverage with examples. Key moments:
    - 26:40-26:42
    - 29:42-29:44
    - 29:58-30:00
    - Tip: Open Video 18 and jump to around 26:40

If you want the main teaching segment, go to Video 18
```

## Technology Stack

- Embeddings: Ollama BGE-M3
- AI: OpenAI GPT-4
- Search: Cosine Similarity with scikit-learn
- Storage: Joblib
- Transcription: OpenAI Whisper
- Video Processing: FFmpeg

## License

This project is for educational purposes.

## Support

For issues or questions, check the troubleshooting section above or open an issue on the project repository.
