import os
from faster_whisper import WhisperModel

# Load the faster-whisper base model on CPU using int8 quantization
model = WhisperModel("base", device="cpu", compute_type="int8")


# Transcribe an audio file and return the full text, word timestamps, and duration
def transcribe(audio_path):
    # Stop early if the file is missing
    if not os.path.exists(audio_path):
        print(f"File not found: {audio_path}")
        return {"text": "", "words": [], "duration": 0.0}

    try:
        segments, info = model.transcribe(audio_path, word_timestamps=True)
        words = []
        full_text = []

        for segment in segments:
            full_text.append(segment.text.strip())
            if segment.words:
                for w in segment.words:
                    words.append({
                        "word": w.word.strip(),
                        "start": round(float(w.start), 2),
                        "end": round(float(w.end), 2),
                    })

        return {
            "text": " ".join(full_text).strip(),
            "words": words,
            "duration": round(float(info.duration), 2),
        }
    except Exception as e:
        # Show the real error so we can debug it
        print(f"Transcription error: {e}")
        return {"text": "", "words": [], "duration": 0.0}