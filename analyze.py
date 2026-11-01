import string

# Thresholds and point deductions for the delivery score
PAUSE_THRESHOLD_SEC = 1.5
MIN_WPM = 120
MAX_WPM = 160
FILLER_PENALTY = 3
PAUSE_PENALTY = 5
PACE_PENALTY = 10

SINGLE_FILLERS = {"um", "uh", "basically"}
NON_FILLER_BEFORE_LIKE = {"i", "you", "we", "they", "would", "look", "looks", "feel", "feels", "sound", "sounds"}


# Calculate a delivery score out of 100 based on fillers, speaking pace, and long pauses
def calculate_score(fillers, wpm, pauses):
    score = 100

    # Deduct points for each filler word used
    score -= fillers * FILLER_PENALTY

    # Deduct points for each pause longer than PAUSE_THRESHOLD_SEC
    score -= pauses * PAUSE_PENALTY

    # Deduct points if speaking speed is slower than MIN_WPM or faster than MAX_WPM
    if wpm < MIN_WPM or wpm > MAX_WPM:
        score -= PACE_PENALTY

    return max(0, min(100, int(score)))


# Analyze the transcript dictionary for fillers, WPM, long pauses, and overall score
def analyze(transcript_dict):
    words = transcript_dict.get("words", [])
    duration = transcript_dict.get("duration", 0.0)

    if not words or duration <= 0:
        return {"fillers": 0, "filler_list": [], "wpm": 0.0, "pauses": 0, "score": 0}

    # Lowercase each word and strip punctuation before matching fillers
    clean_words = [w["word"].lower().strip(string.punctuation) for w in words]
    filler_list = []

    for i, word in enumerate(clean_words):
        if word in SINGLE_FILLERS:
            filler_list.append(word)
        elif word == "you" and i + 1 < len(clean_words) and clean_words[i + 1] == "know":
            filler_list.append("you know")
        # Limitation: only checks the previous word to skip phrases like "I like", "would like", or "looks like"
        elif word == "like":
            prev_word = clean_words[i - 1] if i > 0 else ""
            if prev_word not in NON_FILLER_BEFORE_LIKE:
                filler_list.append("like")

    # Count gaps longer than 1.5 seconds between consecutive words
    pauses = 0
    for i in range(len(words) - 1):
        gap = words[i + 1]["start"] - words[i]["end"]
        if gap > PAUSE_THRESHOLD_SEC:
            pauses += 1

    # Calculate words per minute: total words / (duration in minutes)
    wpm = round(len(words) / (duration / 60.0), 1)
    fillers = len(filler_list)
    score = calculate_score(fillers, wpm, pauses)

    return {
        "fillers": fillers,
        "filler_list": filler_list,
        "wpm": wpm,
        "pauses": pauses,
        "score": score,
    }