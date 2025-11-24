# RAG-Based Course Teaching Assistant

A web-based RAG (Retrieval Augmented Generation) system that helps students find specific content in course videos by answering questions with precise video references and timestamps.

## Project Overview

This system processes course videos, extracts transcripts, creates embeddings, and provides an intelligent Q&A interface where students can ask questions and get directed to specific video segments.

## Features

- Video to audio conversion
- Audio transcription with timestamps using OpenAI Whisper
- Semantic search using BGE-M3 embeddings via Ollama
- AI-powered responses with GPT-4
- Web interface for easy interaction
- Precise video references with timestamps

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

### 4. Configure API Keys

Create a .env file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Project Structure

```
project/
├── videos/                    # Place your video files here
├── audios/                    # Converted audio files
├── compressed_audios/         # Compressed audio files
├── jsons/                     # Transcript JSON files with timestamps
├── templates/                 # HTML templates for web interface
│   └── index.html
├── app.py                     # Flask web application
├── videos_to_mp3.py          # Convert videos to MP3
├── compress.py               # Compress audio files
├── mp3_to_json.mp3.py        # Transcribe audio to JSON
├── preprocess_json.py        # Create embeddings
├── process_incoming.py       # CLI version for testing
├── merge_chunks.py           # Optional: merge small chunks
├── config.py                 # Configuration file
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Usage

### Step 1: Prepare Your Videos

Place all course video files in the videos/ folder. Supported formats: MP4, MKV, AVI, MOV, FLV

### Step 2: Convert Videos to Audio

```bash
python videos_to_mp3.py
```

This creates MP3 files in the audios/ folder.

### Step 3: Compress Audio Files

```bash
python compress.py
```

This compresses audio files to 64k bitrate and saves them in compressed_audios/ folder.

### Step 4: Transcribe Audio to JSON

```bash
python mp3_to_json.mp3.py
```

This uses OpenAI Whisper API to transcribe audio with timestamps and saves JSON files in jsons/ folder.

### Step 5: Create Embeddings

Make sure Ollama is running, then:

```bash
python preprocess_json.py
```

This creates embeddings.joblib file containing all video chunk embeddings.

### Step 6: Run the Web Application

```bash
python app.py
```

Open your browser and go to: http://localhost:5000

### Alternative: Command Line Interface

For testing without the web interface:

```bash
python process_incoming.py
```

## How It Works

1. Videos are converted to audio files
2. Audio is transcribed using OpenAI Whisper API with timestamps
3. Transcripts are split into chunks with time ranges
4. Each chunk is converted to embeddings using BGE-M3 model
5. User questions are converted to embeddings
6. System finds most similar chunks using cosine similarity
7. Relevant chunks are sent to GPT-4 for natural language response
8. Response includes video numbers and timestamps

## Video File Naming Convention

Name your video files as: `number_title.extension`

Example: `01_Introduction to ML.mp4`

This helps the system organize and reference videos correctly.

## API Endpoints

### POST /api/ask
Submit a question and get an answer with video references.

Request body:
```json
{
  "query": "where is univariate analysis taught"
}
```

Response:
```json
{
  "response": "AI generated answer text",
  "relevant_chunks": [
    {
      "title": "Video title",
      "number": "video number",
      "start": "MM:SS",
      "end": "MM:SS",
      "start_seconds": 123,
      "text": "transcript text"
    }
  ]
}
```

### GET /api/health
Check if the server is running and embeddings are loaded.

### GET /api/videos
Get list of all videos in the system.

## Configuration

### Change Number of Search Results

In app.py, modify the top_k parameter:

```python
relevant_chunks = search_relevant_chunks(query, top_k=5)
```

### Change Compression Quality

In compress.py, modify the bitrate:

```python
"-b:a", "64k"  # Change to 96k or 128k for better quality
```

### Merge Small Chunks

If transcript chunks are too small, use merge_chunks.py to combine them:

```bash
python merge_chunks.py
```

This merges every 5 chunks into one. Modify the variable n in the script to change this.

## Troubleshooting

### Problem: Embeddings not loading

Solution: Make sure you ran preprocess_json.py and embeddings.joblib file exists

### Problem: Ollama connection error

Solution: Start Ollama server with `ollama serve` and ensure it is running on port 11434

### Problem: OpenAI API error

Solution: Check that your API key in .env file is valid and has credits

### Problem: FFmpeg not found

Solution: Install FFmpeg and ensure it is in your system PATH

### Problem: Port 5000 already in use

Solution: Change the port in app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Cost Considerations

- OpenAI Whisper API: Charged per minute of audio transcribed
- OpenAI GPT-4 API: Charged per token used
- Ollama: Free, runs locally

Estimate costs before processing large amounts of content.

## Limitations

- Ollama must run locally
- Requires decent RAM for embeddings (500MB+ for 100 videos)
- OpenAI API requires internet connection
- Processing time depends on video length

## Security

Never commit .env file or API keys to version control.

Add to .gitignore:
```
.env
*.joblib
audios/
videos/
compressed_audios/
jsons/
__pycache__/
```

## Future Improvements

- Add video player integration
- Implement user authentication
- Add chat history
- Support multiple courses
- Add caching for frequent queries
- Implement batch processing for large datasets

## License

This project is for educational purposes.

## Support

For issues or questions, check the troubleshooting section above.