"""
Example Python code demonstrating podcast generation directly from a script.
Podfeed in this case acts simply as a text-to-speech service.
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

    # You must have one turn per line. Every line must start with either HOST: or COHOST:
    # HOST and COHOST lines must alternate. You cannot have either HOST or COHOST speak twice in a row.
    # For monologue audio generation, you do not need any prefixes or special structure.
    dialogue_script = """HOST: Hello, how are you?
COHOST: I'm doing great, thank you! How about you?
HOST: I'm doing well, thanks for asking.
COHOST: That's great to hear!
"""

    try:
        # Generate audio directly from provided script (text-to-speech only)
        result = client.generate_audio(
            request=AudioGenerationRequest(
                input_type="script",
                mode="dialogue",
                input_content=InputContent(script=dialogue_script),
                voice_config=VoiceConfig(host_voice="shimmer", cohost_voice="echo"),
                content_config=ContentConfig(
                    language="en-US",
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
