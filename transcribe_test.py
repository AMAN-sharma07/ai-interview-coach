
    
    
import sys
from transcribe import transcribe


# Run a quick test on an audio file and print the returned dictionary
def main():
    audio_path = sys.argv[1] if len(sys.argv) > 1 else "sample.wav"
    print(f"Transcribing: {audio_path} ...")
    result = transcribe(audio_path)

    print("\n--- TRANSCRIPT RESULT ---")
    print("Text:", result["text"])
    print("Duration (seconds):", result["duration"])
    print("Total words:", len(result["words"]))
    print("First 5 words:", result["words"][:5])


if __name__ == "__main__":
    main()