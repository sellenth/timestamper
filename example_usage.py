#!/usr/bin/env python3
"""
Example usage of the Video Timestamper
"""

from video_timestamper import VideoTimestamper
import json

# Example 1: Basic usage with default 30-minute intervals
def example_basic():
    print("Example 1: Basic Usage")
    print("-" * 50)
    
    timestamper = VideoTimestamper()
    
    # Replace with your YouTube URL
    youtube_url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
    
    timestamps = timestamper.generate_timestamps(youtube_url)
    
    # Print each timestamp
    for ts in timestamps:
        print(f"{ts['timestamp']} - {ts['description']}")
    print()


# Example 2: Custom intervals and save to file
def example_custom_interval():
    print("Example 2: Custom 20-minute intervals with file output")
    print("-" * 50)
    
    timestamper = VideoTimestamper()
    youtube_url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Generate timestamps every 20 minutes
    timestamps = timestamper.generate_timestamps(youtube_url, interval_minutes=20)
    
    # Save formatted output
    formatted = timestamper.format_output(timestamps, save_to_file="rickroll_timestamps.txt")
    print("Output saved to rickroll_timestamps.txt and rickroll_timestamps.json")
    print()


# Example 3: Process multiple videos
def example_batch_processing():
    print("Example 3: Batch processing multiple videos")
    print("-" * 50)
    
    timestamper = VideoTimestamper()
    
    video_urls = [
        "https://youtube.com/watch?v=VIDEO_ID_1",
        "https://youtube.com/watch?v=VIDEO_ID_2",
        "https://youtube.com/watch?v=VIDEO_ID_3"
    ]
    
    all_timestamps = {}
    
    for url in video_urls:
        video_id = url.split("v=")[-1]
        print(f"Processing video: {video_id}")
        
        try:
            timestamps = timestamper.generate_timestamps(url)
            all_timestamps[video_id] = timestamps
            print(f"✓ Generated {len(timestamps)} timestamps")
        except Exception as e:
            print(f"✗ Error: {e}")
        print()
    
    # Save all results to a single JSON file
    with open("batch_timestamps.json", "w") as f:
        json.dump(all_timestamps, f, indent=2)
    print("Batch results saved to batch_timestamps.json")


# Example 4: Custom prompt for specific content types
def example_custom_prompt():
    print("Example 4: Custom analysis for specific content")
    print("-" * 50)
    
    # For this example, we'd need to modify the VideoTimestamper class
    # to accept custom prompts. Here's how you might use it:
    
    timestamper = VideoTimestamper()
    
    # You could extend the class to support custom prompts like:
    # timestamper.set_custom_prompt("Focus on technical concepts and coding moments")
    
    print("This example shows how you might extend the class for specific use cases")
    print("like technical tutorials, cooking shows, or gaming streams")


if __name__ == "__main__":
    print("Video Timestamper Examples")
    print("=" * 50)
    print()
    
    # Uncomment the example you want to run:
    
    # example_basic()
    # example_custom_interval()
    # example_batch_processing()
    # example_custom_prompt()
    
    print("\nNote: Replace example URLs with your actual YouTube video URLs")
    print("Make sure GEMINI_API_KEY is set in your environment")