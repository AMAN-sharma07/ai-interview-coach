AI Interview Coach

A lightweight, CPU-friendly AI interview coaching application built with Python, Streamlit, faster-whisper, and Google Gemini.

The app lets students practice common interview questions, record or upload spoken responses, and receive instant feedback on speaking delivery (filler words, pace, long pauses, score) and answer quality (relevance rating, actionable tips, and an improved sample answer).

Architecture Pipeline

User Speech (Mic / Upload)
           │
           ▼
faster-whisper (CPU, int8)  ──► Transcript & Word Timestamps
           │
           ├──────────────────► Deterministic Analysis (WPM, Fillers, Pauses, Score)
           │
           ▼
Gemini 3.8 Flash (GenAI SDK) ──► Relevance Rating, Tips & Sample Answer
           │
           ▼
Streamlit Interactive Dashboard


Tech Stack

Python 3.10+

Streamlit: Web interface for audio input and dashboard metrics.

faster-whisper: Offline speech-to-text with word-level timestamps running on CPU (base model, int8 quantization).

Google GenAI SDK (google-genai): Answer relevance rating and coaching suggestions powered by gemini-3.8-flash.

File Structure

├── app.py            # Streamlit dashboard and pipeline orchestration
├── transcribe.py     # Speech-to-text transcription with word timestamps
├── analyze.py        # Delivery metrics (WPM, pauses, fillers, score)
├── feedback.py       # Gemini API client for structured coaching feedback
├── questions.py      # Curated list of common interview questions
├── requirements.txt  # Pinned dependencies
└── README.md         # Project documentation


Getting Started

1. Prerequisites

Python 3.10, 3.11, or 3.12

FFmpeg:

Windows (PowerShell):

winget install Gyan.FFmpeg


macOS (Homebrew):

brew install ffmpeg


Linux (Ubuntu/Debian):

sudo apt update && sudo apt install ffmpeg


2. Clone the Repository & Install Dependencies

git clone https://github.com/<your-username>/ai-interview-coach.git
cd ai-interview-coach
pip install -r requirements.txt


3. Set Your Gemini API Key

Obtain a free API key from Google AI Studio.

Windows PowerShell:

$env:GEMINI_API_KEY = "your_actual_api_key_here"


Linux / macOS:

export GEMINI_API_KEY="your_actual_api_key_here"


4. Run the Application

streamlit run app.py


Open http://localhost:8501 in your browser.

Delivery Score Formula

The delivery score starts at 100 and applies transparent deductions:

-3 points per filler word ("um", "uh", "basically", "you know", or contextual "like").

-5 points per pause longer than 1.5 seconds.

-10 points if overall pace is outside the comfortable conversational range (120–160 WPM).