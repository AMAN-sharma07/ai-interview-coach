from feedback import get_feedback


# Send a sample question and transcript to Gemini and print the returned dictionary
def main():
    sample_question = "Tell me about a challenge you faced on a project and how you solved it."
    sample_transcript = (
        "Um, in my database class project, our queries were running really slowly. "
        "I looked at the query plan, added an index on the user ID column, and it ran much faster."
    )

    print("Sending sample answer to Gemini...")
    result = get_feedback(sample_question, sample_transcript)

    print("\n--- GEMINI FEEDBACK RESULT ---")
    print("Rating (1-10):", result["rating"])
    print("Strengths / Tips:", result["strengths"])
    print("Improved Answer:", result["improved_answer"])


if __name__ == "__main__":
    main()