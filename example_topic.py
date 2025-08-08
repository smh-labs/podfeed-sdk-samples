"""
Example Python code demonstrating podcast generation from a given topic.
Podfeed will run a research on the topic and generate a podcast.
"""

import os
import sys
from podfeed import (
    PodfeedClient,
    PodfeedError,
    AudioGenerationRequest,
    InputContent,
    VoiceConfig,
    ContentConfig,
)


def main():
    # Initialize client
    api_key = os.getenv("PODFEED_API_KEY")
    if not api_key:
        print("Error: PODFEED_API_KEY environment variable not set")
        return 1

    client = PodfeedClient(api_key=api_key)

    topic = "Vibe coding best practices"

    try:
        # Generate audio directly from provided script (text-to-speech only)
        result = client.generate_audio(
            request=AudioGenerationRequest(
                input_type="topic",
                mode="dialogue",
                input_content=InputContent(topic=topic),
                voice_config=VoiceConfig(
                    host_voice="gemini-achernar",
                    cohost_voice="gemini-achird",
                    host_voice_instructions="Speak with a calm, gentle tone.",
                    cohost_voice_instructions="Speak nervously, as if anxious about the future.",
                ),
                content_config=ContentConfig(
                    level="beginner",
                    length="medium",
                    language="en-US",
                    questions="What are the best models for coding?",
                    user_instructions="Explain it to someone who doesn't have experience coding, but already knows what vibe coding is.",
                    emphasis="tactics, tips and tricks",
                ),
            )
        )

        print(f"Audio generation started successfully!")
        print(f"Task ID: {result['task_id']}")
        print(f"Status: {result['status']}")

        # Wait for completion
        print("\nWaiting for audio generation to complete...")
        final_result = client.wait_for_completion(result["task_id"])

        print("Audio generation completed!")
        print(f"Final status: {final_result}")

    except PodfeedError as e:
        print(f"Podfeed API Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
