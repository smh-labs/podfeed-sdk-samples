"""
Example: Pre-add generated audio to a feed, and manage feeds.
Demonstrates feedId for auto-add, and feed management APIs.
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
    api_key = os.getenv("PODFEED_API_KEY")
    if not api_key:
        print("Error: PODFEED_API_KEY environment variable not set")
        return 1

    client = PodfeedClient(api_key=api_key)

    try:
        # List existing feeds
        feeds_resp = client.list_feeds()
        feeds = feeds_resp.get("feeds", [])
        feed_id = feeds[0]["id"] if feeds else None

        if not feed_id:
            # Create a feed if none exists
            print("No feeds found. Creating a new feed...")
            create_resp = client.create_feed(
                name="My Tech Podcast",
                description="AI-generated tech content",
            )
            feed_id = create_resp["feed"]["id"]
            print(f"Created feed: {feed_id}")

        # Generate audio and pre-add to feed using feedId
        result = client.generate_audio(
            request=AudioGenerationRequest(
                input_type="topic",
                input_content=InputContent(
                    topic="Latest developments in quantum computing"
                ),
                mode="dialogue",
                voice_config=VoiceConfig(
                    host_voice="elevenlabs-mark",
                    cohost_voice="elevenlabs-cassidy",
                ),
                content_config=ContentConfig(
                    level="intermediate",
                    length="short",
                    language="en-US",
                ),
                feed_id=feed_id,  # Auto-add to feed when generation completes
            )
        )

        print(f"Audio generation started (will be added to feed {feed_id})")
        print(f"Task ID: {result['task_id']}")

        final_result = client.wait_for_completion(result["task_id"])
        audio_id = final_result.get("result", {}).get("audio_id")

        if audio_id:
            print(f"Audio generated and added to feed: {audio_id}")
            # Fetch feed to see the new episode
            feed = client.get_feed(feed_id)
            print(f"Feed now has {feed['feed'].get('episode_count', 0)} episodes")
        else:
            print("Or add an existing audio manually:")
            print(
                "  client.add_audio_to_feed(audio_id='...', feed_id='...', "
                "episode_title='My Episode')"
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
