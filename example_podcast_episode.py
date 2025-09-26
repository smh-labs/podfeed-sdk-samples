"""
Example Python code demonstrating podcast generation from a Youtube video.
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

    try:
        # Example Apple Podcast URL (Andrew Huberman's podcast episode)
        podcast_ep_url = "https://podcasts.apple.com/se/podcast/essentials-adhd-how-anyone-can-improve-their-focus/id1545953110?i=1000719965062&l=en-GB"

        # Generate audio from website
        result = client.generate_audio(
            request=AudioGenerationRequest(
                input_type="url",
                mode="monologue",
                input_content=InputContent(url=podcast_ep_url),
                voice_config=VoiceConfig(voice="elevenlabs-joe"),  # ASMR voice
                content_config=ContentConfig(
                    level="beginner",
                    length="short",
                    language="en-US",
                    questions="",
                    user_instructions="Explain the key points in the style of Joe Rogan",
                    emphasis="",
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

        print(f"Audio URL: {final_result.get('audio_url')}")

    except PodfeedError as e:
        print(f"Podfeed API Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
