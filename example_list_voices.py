#!/usr/bin/env python3
"""
Example script demonstrating how to list and use available voices in the Podfeed Python SDK.

This script shows how to:
1. List all available voices
2. Filter voices by language and TTS provider
3. Find suitable voices for your use case
4. Use voices in audio generation
"""

import os
import sys
from typing import Dict, List
from podfeed import PodfeedClient, PodfeedError


def display_voice_info(voice_id: str, voice_data: Dict) -> None:
    """Display formatted information about a voice."""
    print(f"  🎤 {voice_id}")
    print(f"     Provider: {voice_data.get('tts', 'unknown').upper()}")
    print(f"     Display Name: {voice_data.get('display_name', 'N/A')}")
    print(f"     Credits Multiplier: {voice_data.get('credits_multiplier', 1.0)}x")
    if voice_data.get("description"):
        print(f"     Description: {voice_data['description']}")
    print()


def filter_voices_by_provider(
    voices_config: Dict, provider: str
) -> Dict[str, List[str]]:
    """Filter voices by TTS provider."""
    filtered = {}
    for lang_code, lang_data in voices_config.items():
        lang_voices = []
        for voice_id, voice_data in lang_data.get("voices", {}).items():
            if voice_data.get("tts") == provider.lower():
                lang_voices.append(voice_id)
        if lang_voices:
            filtered[lang_code] = lang_voices
    return filtered


def find_affordable_voices(
    voices_config: Dict, max_multiplier: float = 1.5
) -> Dict[str, List[str]]:
    """Find voices with credits multiplier below threshold."""
    affordable = {}
    for lang_code, lang_data in voices_config.items():
        lang_voices = []
        for voice_id, voice_data in lang_data.get("voices", {}).items():
            if voice_data.get("credits_multiplier", 1.0) <= max_multiplier:
                lang_voices.append(voice_id)
        if lang_voices:
            affordable[lang_code] = lang_voices
    return affordable


def main():
    # Initialize client
    api_key = os.getenv("PODFEED_API_KEY")
    if not api_key:
        print("Error: PODFEED_API_KEY environment variable not set")
        return 1

    client = PodfeedClient(api_key=api_key)

    try:
        print("🔍 Fetching available voices...")
        voices_config = client.list_available_voices()

        print(f"\n📊 Found voices in {len(voices_config)} languages\n")

        # Display all voices organized by language
        for lang_code, lang_data in voices_config.items():
            language_name = lang_data.get("language_name", lang_code.upper())
            voices = lang_data.get("voices", {})

            print(f"🌍 {language_name} ({lang_code}) - {len(voices)} voices:")

            for voice_id, voice_data in voices.items():
                display_voice_info(voice_id, voice_data)

        # Filter examples
        print("=" * 60)
        print("🔍 FILTERING EXAMPLES")
        print("=" * 60)

        # Find Google voices
        google_voices = filter_voices_by_provider(voices_config, "google")
        if google_voices:
            print(f"\n🤖 Google voices available in {len(google_voices)} languages:")
            for lang, voices in google_voices.items():
                print(f"  {lang}: {len(voices)} voices")

        # Find ElevenLabs voices
        elevenlabs_voices = filter_voices_by_provider(voices_config, "elevenlabs")
        if elevenlabs_voices:
            print(
                f"\n🎭 ElevenLabs voices available in {len(elevenlabs_voices)} languages:"
            )
            for lang, voices in elevenlabs_voices.items():
                print(f"  {lang}: {len(voices)} voices")

        # Find affordable voices (low cost multiplier)
        affordable_voices = find_affordable_voices(voices_config, max_multiplier=1.5)
        if affordable_voices:
            print(
                f"\n💰 Affordable voices (≤1.5x cost) in {len(affordable_voices)} languages:"
            )
            for lang, voices in affordable_voices.items():
                print(f"  {lang}: {len(voices)} voices")

        # Example: Generate audio with a specific voice
        if "en" in voices_config and voices_config["en"].get("voices"):
            english_voices = voices_config["en"]["voices"]
            # Get the first available English voice
            sample_voice = list(english_voices.keys())[0]

            print(f"\n🎵 EXAMPLE: Using voice '{sample_voice}' for audio generation")
            print(
                f"Provider: {english_voices[sample_voice].get('tts', 'unknown').upper()}"
            )
            print(
                f"Cost multiplier: {english_voices[sample_voice].get('credits_multiplier', 1.0)}x"
            )

            print("\nExample generate_audio call:")
            print(
                f"""
result = client.generate_audio(
    input_type="topic",
    topic="Introduction to renewable energy",
    mode="monologue",
    voice="{sample_voice}",
    language="en",
    level="intermediate"
)
            """
            )

    except PodfeedError as e:
        print(f"Podfeed API Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
