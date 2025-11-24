from flask import Flask, render_template, request, jsonify, stream_with_context, Response
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import requests
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Load embeddings
try:
    df = joblib.load('embeddings.joblib')
    print("✓ Embeddings loaded successfully")
except Exception as e:
    print(f"✗ Error loading embeddings: {e}")
    df = None


def create_embedding(text_list):
    """Create embeddings using Ollama BGE-M3 model"""
    try:
        r = requests.post("http://localhost:11434/api/embed", json={
            "model": "bge-m3",
            "input": text_list
        }, timeout=30)
        embedding = r.json()["embeddings"]
        return embedding
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return None


def search_relevant_chunks(query, top_k=5):
    """Search for relevant video chunks based on query"""
    if df is None:
        return None
    
    # Create embedding for the query
    question_embedding = create_embedding([query])
    if question_embedding is None:
        return None
    
    question_embedding = question_embedding[0]
    
    # Calculate cosine similarities
    similarities = cosine_similarity(
        np.vstack(df['embedding']), 
        [question_embedding]
    ).flatten()
    
    # Get top results
    top_indices = similarities.argsort()[::-1][:top_k]
    results = df.loc[top_indices]
    
    return results


def generate_response(query, relevant_chunks):
    """Generate response using OpenAI API"""
    prompt = f'''I am teaching a Machine Learning Course. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, and the text at that time:

{relevant_chunks[["title", "number", "start", "end", "text"]].to_json(orient="records")}
---------------------------------
User Question: "{query}"

You are a helpful teaching assistant. Based on the video chunks provided:
1. Answer the user's question in a conversational, human way
2. Guide them to specific videos and timestamps where the content is taught
3. Format timestamps as MM:SS (e.g., 11:17 for 677 seconds)
4. If the question is unrelated to the course content, politely inform them you can only answer questions related to the course

Provide a clear, structured response.'''

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful teaching assistant for a Machine Learning course."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return None


def format_timestamp(seconds):
    """Convert seconds to MM:SS format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Handle question from user"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Query cannot be empty'}), 400
    
    if df is None:
        return jsonify({'error': 'Embeddings not loaded. Please run preprocess_json.py first.'}), 500
    
    # Search for relevant chunks
    relevant_chunks = search_relevant_chunks(query, top_k=5)
    
    if relevant_chunks is None or len(relevant_chunks) == 0:
        return jsonify({'error': 'Could not find relevant content'}), 500
    
    # Generate response
    response_text = generate_response(query, relevant_chunks)
    
    if response_text is None:
        return jsonify({'error': 'Could not generate response'}), 500
    
    # Format relevant chunks for display
    chunks_data = []
    for _, chunk in relevant_chunks.iterrows():
        chunks_data.append({
            'title': chunk['title'],
            'number': chunk['number'],
            'start': format_timestamp(chunk['start']),
            'end': format_timestamp(chunk['end']),
            'start_seconds': int(chunk['start']),
            'text': chunk['text']
        })
    
    return jsonify({
        'response': response_text,
        'relevant_chunks': chunks_data
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if the service is running"""
    return jsonify({
        'status': 'running',
        'embeddings_loaded': df is not None,
        'total_chunks': len(df) if df is not None else 0
    })


@app.route('/api/videos', methods=['GET'])
def get_videos():
    """Get list of all videos in the system"""
    if df is None:
        return jsonify({'error': 'Embeddings not loaded'}), 500
    
    videos = df.groupby(['number', 'title']).size().reset_index(name='chunk_count')
    videos_list = videos.to_dict('records')
    
    return jsonify({'videos': videos_list})


if __name__ == '__main__':
    print("="*50)
    print("Course RAG Assistant Server")
    print("="*50)
    print(f"Embeddings loaded: {df is not None}")
    if df is not None:
        print(f"Total chunks: {len(df)}")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)