# Podfeed SDK Samples

Example scripts demonstrating the [Podfeed Python SDK](https://github.com/smh-labs/podfeed-sdk-python) for generating podcast-style audio content from various input sources.

## Prerequisites

1. **Install the SDK**:
   ```bash
   pip install podfeed-sdk
   ```

2. **Get an API key** from [podfeed.ai](https://podfeed.ai) (log in, then go to the API section).

3. **Set the API key**:
   ```bash
   export PODFEED_API_KEY="your-api-key-here"
   ```

## Quick Start

### Generate Audio (from Website)

```python
from podfeed import (
    PodfeedClient,
    PodfeedError,
    AudioGenerationRequest,
    InputContent,
    VoiceConfig,
    ContentConfig,
)

# Initialize client (uses PODFEED_API_KEY env var)
client = PodfeedClient()

# Example URL
website_url = "https://podfeed.ai/faq"

# Generate audio from website
result = client.generate_audio(
    request=AudioGenerationRequest(
        input_type="url",
        mode="dialogue",
        input_content=InputContent(url=website_url),
        voice_config=VoiceConfig(
            host_voice="gemini-puck", cohost_voice="gemini-achird"
        ),
        content_config=ContentConfig(
            level="intermediate",
            length="medium",
            language="en-US",
            questions="What kind of content can I use with Podfeed?",
        ),
    )
)

task_id = result["task_id"]
print(f"Task created: {task_id}")

# Wait for completion
final = client.wait_for_completion(task_id)
print(f"Audio generated: {final['result']['audio_url']}")
```

### List Available Voices

```python
from podfeed import PodfeedClient

client = PodfeedClient()  # uses PODFEED_API_KEY env var

voices = client.list_available_voices()
for lang_code, lang_data in voices.items():
    print(f"{lang_data['language_name']} ({lang_code}):")
    for voice_id, info in lang_data["voices"].items():
        print(f"  {voice_id} - {info.get('tts', 'unknown')} ({info.get('credits_multiplier', 1.0)}x credits)")
```

## Examples

Each example is a standalone script. Run any example with:

```bash
python example_website.py
```

* `example_bring_your_own_script.py`: Generate audio from your own script, using Podfeed as a text-to-speech service only.
* `example_combined_sources.py`: **New** - Combine multiple sources (text + URL + file) in one request.
* `example_feed_and_preadd.py`: **New** - Pre-add generated audio to a feed, create feeds, and manage episodes.
* `example_files.py`: Generate an audio podcast from local files (PDF, audio, and video files are supported)
* `example_list_voices.py`: Demonstrates how to list available voices and filter by cost
* `example_podcast_episode.py`: Generate a podcast from a real podcast episode (must be an Apple Podcast or Spotify Podcast episode URL)
* `example_topic.py`: Generate a podcast from a given topic. Podfeed will research the topic first and generate the audio based on the report.
* `example_website.py`: Generate a podcast from a website URL.
* `example_youtube.py`: Generate a podcast from a Youtube video URL.

## Error Handling

```python
from podfeed import PodfeedClient, PodfeedError, PodfeedAuthError, PodfeedAPIError
from podfeed import AudioGenerationRequest, InputContent, VoiceConfig

try:
    client = PodfeedClient()
    task = client.generate_audio(
        request=AudioGenerationRequest(
            input_type="text",
            mode="monologue",
            input_content=InputContent(text="Sample text content here."),
            voice_config=VoiceConfig(voice="gemini-achird"),
        )
    )
    result = client.wait_for_completion(task["task_id"])
except PodfeedAuthError as e:
    print(f"Authentication error: {e}")
except PodfeedAPIError as e:
    print(f"API error: {e.message} (Status: {e.status_code})")
except PodfeedError as e:
    print(f"General error: {e}")
```

## SDK Documentation

For the full SDK reference, see the [Podfeed Python SDK README](https://github.com/smh-labs/podfeed-sdk-python).

For API documentation, visit [podfeed.ai/developers](https://podfeed.ai/developers).

## Requirements

- Python 3.7+
- `podfeed-sdk` (install via `pip install podfeed-sdk`)

## Support

- **SDK Documentation**: [github.com/smh-labs/podfeed-sdk-python](https://github.com/smh-labs/podfeed-sdk-python)
- **API Documentation**: [podfeed.ai/developers](https://podfeed.ai/developers)
- **Email**: support@podfeed.ai
