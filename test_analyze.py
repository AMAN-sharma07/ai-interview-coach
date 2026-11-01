from analyze import analyze


# Test analyze() using a hardcoded transcript dictionary without needing audio
def main():
    sample_transcript = {
        "text": "Um, I like Python and, you know, I would like to build, like, web apps. Basically, it looks like fun.",
        "words": [
            {"word": "Um,", "start": 0.0, "end": 0.4},
            {"word": "I", "start": 0.5, "end": 0.6},
            {"word": "like", "start": 0.6, "end": 0.9},        # Not a filler ("I like")
            {"word": "Python", "start": 0.9, "end": 1.3},
            {"word": "and,", "start": 1.3, "end": 1.6},
            {"word": "you", "start": 3.5, "end": 3.7},         # 1.9s pause before "you", start of "you know"
            {"word": "know,", "start": 3.7, "end": 4.0},
            {"word": "I", "start": 4.1, "end": 4.2},
            {"word": "would", "start": 4.2, "end": 4.5},
            {"word": "like", "start": 4.5, "end": 4.8},        # Not a filler ("would like")
            {"word": "to", "start": 4.8, "end": 4.9},
            {"word": "build,", "start": 4.9, "end": 5.3},
            {"word": "like,", "start": 5.4, "end": 5.7},       # Filler ("build, like,")
            {"word": "web", "start": 5.8, "end": 6.1},
            {"word": "apps.", "start": 6.1, "end": 6.5},
            {"word": "Basically,", "start": 8.3, "end": 8.9},  # 1.8s pause before "Basically," + filler
            {"word": "it", "start": 9.0, "end": 9.1},
            {"word": "looks", "start": 9.1, "end": 9.4},
            {"word": "like", "start": 9.4, "end": 9.7},        # Not a filler ("looks like")
            {"word": "fun.", "start": 9.7, "end": 10.0},
        ],
        "duration": 10.0,
    }

    result = analyze(sample_transcript)
    print("--- ANALYSIS RESULT ---")
    print(result)


if __name__ == "__main__":
    main()