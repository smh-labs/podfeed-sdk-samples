"""
Example Python code demonstrating podcast generation from files.
"""

import os
import sys
from pathlib import Path
from podfeed import (
    PodfeedClient,
    PodfeedError,
    AudioGenerationRequest,
    InputContent,
    VoiceConfig,
    ContentConfig,
)


def progress_callback(current: int, total: int):
    """Progress callback for file uploads."""
    percentage = (current / total) * 100
    print(f"Upload progress: {current}/{total} files ({percentage:.1f}%)")


def main():
    # Initialize client
    api_key = os.getenv("PODFEED_API_KEY")
    if not api_key:
        print("Error: PODFEED_API_KEY environment variable not set")
        return 1

    client = PodfeedClient(api_key=api_key)

    # Example file paths (modify these to point to your actual files)
    file_paths = [
        "sample_content/example_document.pdf",
        "sample_content/research_paper.pdf",
    ]

    # Check if files exist
    existing_files = [f for f in file_paths if Path(f).exists()]
    if not existing_files:
        print(
            "No example files found. Please create some test files or update file_paths."
        )
        print("Expected files:")
        for f in file_paths:
            print(f"  - {f}")
        return 1

    try:
        print(f"Generating audio from {len(existing_files)} files...")

        # Generate audio with file upload
        result = client.generate_audio(
            request=AudioGenerationRequest(
                input_type="file",
                mode="monologue",
                input_content=InputContent(files=existing_files),
                voice_config=VoiceConfig(voice="gemini-achird"),
                content_config=ContentConfig(
                    level="expert",
                    length="short",
                    language="en-US",
                    user_instructions="Create an engaging summary of the key points from these documents.",
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
