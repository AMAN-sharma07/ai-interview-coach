import os
import tempfile
import streamlit as st
from questions import QUESTIONS
from transcribe import transcribe
from analyze import analyze
from feedback import get_feedback


# Render the Streamlit UI and run the transcription, analysis, and feedback pipeline
def main():
    st.set_page_config(page_title="AI Interview Coach", layout="centered")
    st.title("AI Interview Coach")

    question = st.selectbox("1. Choose an interview question:", QUESTIONS)

    st.subheader("2. Record or Upload Your Answer")
    recorded = st.audio_input("Record your answer in the browser")
    uploaded = st.file_uploader("Or upload an audio file", type=["wav", "mp3", "m4a"])
    audio_file = recorded or uploaded

    if not audio_file:
        return

    if not os.environ.get("GEMINI_API_KEY"):
        st.error("Missing GEMINI_API_KEY environment variable. Please set it in your terminal and restart.")
        st.stop()

    # Save the recorded or uploaded audio to a temporary file for faster-whisper
    suffix = os.path.splitext(getattr(audio_file, "name", "audio.wav"))[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(audio_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner("Transcribing audio and generating coaching feedback..."):
            transcript = transcribe(tmp_path)
            if not transcript["text"]:
                st.error("No speech detected in the audio. Please record or upload a clear spoken answer.")
                st.stop()

            metrics = analyze(transcript)
            feedback = get_feedback(question, transcript["text"])
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    st.subheader("3. Delivery Metrics & Score")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Filler Words", metrics["fillers"])
    c2.metric("Pace (WPM)", metrics["wpm"])
    c3.metric("Long Pauses (>1.5s)", metrics["pauses"])
    c4.metric("Delivery Score", f"{metrics['score']}/100")

    if metrics["filler_list"]:
        st.caption("Fillers found: " + ", ".join(metrics["filler_list"]))

    st.subheader("4. Transcript")
    st.write(transcript["text"])

    st.subheader("5. AI Answer Feedback")
    if feedback["rating"] == 0:
        st.error(feedback["improved_answer"])
    else:
        st.metric("Relevance & Clarity Rating", f"{feedback['rating']}/10")
        st.markdown("**Strengths & Tips:**")
        for tip in feedback["strengths"]:
            st.markdown(f"- {tip}")
        st.markdown("**Improved Sample Answer:**")
        st.info(feedback["improved_answer"])


if __name__ == "__main__":
    main()