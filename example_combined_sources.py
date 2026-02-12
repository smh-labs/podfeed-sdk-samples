"""
Example: Generate audio from multiple combined sources (text + URL + optional file).
Combines different content types in a single request for richer podcast content.
"""

import os
import sys
from pathlib import Path
from podfeed import (
    PodfeedClient,
    PodfeedError,
    AudioGenerationRequest,
    SourceItem,
    VoiceConfig,
    ContentConfig,
)


def main():
    api_key = os.getenv("PODFEED_API_KEY")
    if not api_key:
        print("Error: PODFEED_API_KEY environment variable not set")
        return 1

    client = PodfeedClient(api_key=api_key)

    # Combine multiple sources: intro text + Wikipedia URL
    sources = [
        SourceItem(
            input_type="text",
            content="This episode explores artificial intelligence. "
            "We'll discuss its history, current applications, and future potential.",
        ),
        SourceItem(
            input_type="url",
            content="https://en.wikipedia.org/wiki/Artificial_intelligence",
        ),
    ]

    # Optional: add a PDF if you have one
    pdf_path = "sample_content/example_document.pdf"
    if Path(pdf_path).exists():
        sources.append(SourceItem(input_type="file", content=pdf_path))

    try:
        result = client.generate_audio(
            request=AudioGenerationRequest(
                content_type="sources",
                sources_content=sources,
                mode="dialogue",
                voice_config=VoiceConfig(
                    host_voice="gemini-achernar",
                    cohost_voice="gemini-achird",
                ),
                content_config=ContentConfig(
                    level="intermediate",
                    length="medium",
                    language="en-US",
                    user_instructions="Make it accessible for a general audience. "
                    "Focus on practical applications.",
                ),
            )
        )

        print("Audio generation started successfully!")
        print(f"Task ID: {result['task_id']}")
        print(f"Status: {result['status']}")

        print("\nWaiting for audio generation to complete...")
        final_result = client.wait_for_completion(result["task_id"])

        print("Audio generation completed!")
        audio_url = final_result.get("result", {}).get("audio_url")
        if audio_url:
            print(f"Audio URL: {audio_url}")
        else:
            print(f"Result: {final_result}")

    except PodfeedError as e:
        print(f"Podfeed API Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
