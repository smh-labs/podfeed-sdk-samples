# PodFeed SDK

A Python SDK for the PodFeed API, enabling developers to generate high-quality Podcast-style audio content from various input sources using AI.

## Features

- **Multiple Input Types**: Support for text, URLs, files, topics, and bring-your-own-script
- **Audio Generation Modes**: Monologue (single voice) and dialogue (two voices) modes
- **Voice Customization**: Multiple voice options for different languages. Some voices support custom instructions
- **Script Customization**: Adjustable complexity levels, lengths, and emphasis


## Installation

```bash
pip install podfeed-sdk
```


## Authentication

The SDK supports two ways to provide your API key:

1. **Environment Variable**:
   ```bash
   export PODFEED_API_KEY="your-api-key-here"
   ```

2. **Direct initialization**:
   ```python
   from podfeed import PodfeedClient
   
   client = PodfeedClient(api_key="your-api-key-here")
   ```

## Quick Start


### Get an API key
Go to [https://podfeed.ai](https://podfeed.ai), log in, and get an API key.

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
            host_voice="google-male-puck", cohost_voice="google-female-leda"
        ),
        content_config=ContentConfig(
            level="intermediate",
            length="medium",
            language="en-US",
            emphasis="",
            questions="what kind of content can I use with Podfeed?",
            user_instructions=""
        ),
    )
)

task_id = response["task_id"]
print(f"Task created: {task_id}")

# Wait for completion
result = client.wait_for_completion(task_id)
print(f"Audio generated: {result['result']['audio_url']}")
```

### List Available Voices

```python
from podfeed import PodfeedClient

api_key = os.getenv("PODFEED_API_KEY")
if not api_key:
    print("Error: PODFEED_API_KEY environment variable not set")
    return 1

client = PodfeedClient(api_key=api_key)

voices_config = client.list_available_voices()
print(voices_config)
```

## Usage Examples
See the example files in this directory.

* `example_bring_your_own_script.py`: Generate audio from your own script, using Podfeed as a text-to-speech service only.
* `example_files.py`: Generate an audio podcast from local files (PDF, audio, and video files are supported)
* `example_list_voices.py`: Demonstrates how to list available voices and filter by cost
* `example_podcast_episode.py`: Generate a podcast from a real podcast episode (must be an Apple Podcast or Spotify Podcast episode URL)
* `example_topic.py`: Generate a podcast from a given topic. Podfeed will research the topic first and generate the audio based on the report.
* `example_website.py`: Generate a podcast from a website URL. 
* `example_youtube.py`: Generate a podcast from a Youtube video URL.

## Error Handling

```python
from podfeed_sdk import PodfeedClient, PodfeedError, PodfeedAuthError, PodfeedAPIError

try:
    client = PodfeedClient()
    response = client.generate_audio(
        input_type="text",
        text_content="Sample text"
    )
except PodFeedAuthError as e:
    print(f"Authentication error: {e}")
except PodFeedAPIError as e:
    print(f"API error: {e.message} (Status: {e.status_code})")
except PodFeedError as e:
    print(f"General error: {e}")
```

## API Reference
We'll be publishing an API reference and documentation soon.


## Requirements

- Python 3.7+
- requests >= 2.25.0

## Rate Limits
Details coming soon.

## Support

For API support, email support@podfeed.ai.