#!/usr/bin/env python3
"""
Video Timestamper - Extract witty timestamps from long YouTube videos
"""

import json
import os
import sys
import re
from typing import List, Dict
import google.generativeai as genai
from datetime import datetime
from pathlib import Path

# Load .env file if it exists
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value


class VideoTimestamper:
    def __init__(self, api_key: str = None):
        """Initialize with Gemini API key"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Please set GEMINI_API_KEY environment variable or pass api_key")
        
        genai.configure(api_key=self.api_key)
        
        # Configure model without structured output to avoid hallucinations
        generation_config = {
            "temperature": 0.8  # Higher for more creative/humorous output
        }
        
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config=generation_config
        )
    
    def generate_timestamps(self, youtube_url: str, interval_minutes: int = 30) -> List[Dict]:
        """Generate timestamps at specified intervals"""
        
        # Calculate timestamp points for a 2-hour video
        timestamps = []
        for minutes in range(0, 121, interval_minutes):  # 0, 30, 60, 90, 120
            hours = minutes // 60
            mins = minutes % 60
            timestamps.append(f"{hours:02d}:{mins:02d}:00")
        
        timestamp_list = "\n".join([f"- {ts}" for ts in timestamps])
        
        prompt = f"""You are analyzing a specific YouTube video. Look at the actual video content at these EXACT timestamps:
{timestamp_list}

IMPORTANT: This is a technical video about evaluating Claude Code for Godot game development. 
Focus on what the presenter is showing, saying, or demonstrating at each specific timestamp.

For each timestamp, provide output in this exact format:
{{
  "timestamp": "HH:MM:SS",
  "description": "8-15 word description with slightly humorous tone"
}}

Keep descriptions between 8-15 words. Be witty but accurate about THIS specific video.
Describe what you see on screen - code, Godot editor, demonstrations, etc.

Return ONLY a JSON array of these objects, nothing else."""

        try:
            # For YouTube videos, we need to pass the URL as a string directly
            # The Gemini API handles YouTube URLs automatically
            response = self.model.generate_content([
                youtube_url,
                prompt
            ])
            # Clean up response text to ensure valid JSON
            text = response.text.strip()
            # Remove markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            return json.loads(text)
        except Exception as e:
            print(f"Error generating timestamps: {e}")
            print(f"Full error details: {type(e).__name__}: {str(e)}")
            return []
    
    def format_output(self, timestamps: List[Dict], save_to_file: str = None) -> str:
        """Format timestamps for display"""
        output_lines = ["🎬 Video Timestamps\n" + "=" * 50 + "\n"]
        
        for ts in timestamps:
            output_lines.append(f"{ts['timestamp']} - {ts['description']}")
        
        output_lines.append("\n" + "=" * 50)
        output_lines.append(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        formatted = "\n".join(output_lines)
        
        if save_to_file:
            # Save both formatted and JSON versions
            with open(save_to_file, 'w') as f:
                f.write(formatted)
            
            json_file = save_to_file.replace('.txt', '.json')
            with open(json_file, 'w') as f:
                json.dump(timestamps, f, indent=2)
            
            print(f"✅ Saved to {save_to_file} and {json_file}")
        
        return formatted


def normalize_youtube_url(url: str) -> str:
    """Convert various YouTube URL formats to standard format"""
    # Extract video ID from different URL formats
    video_id_match = re.search(r'(?:v=|youtu\.be/|embed/|watch\?v=)([a-zA-Z0-9_-]{11})', url)
    if video_id_match:
        video_id = video_id_match.group(1)
        return f"https://youtube.com/watch?v={video_id}"
    return url


def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python video_timestamper.py <youtube_url> [interval_minutes]")
        print("Example: python video_timestamper.py https://youtube.com/watch?v=xxx 30")
        print("         python video_timestamper.py https://youtu.be/xxx 30")
        sys.exit(1)
    
    youtube_url = normalize_youtube_url(sys.argv[1])
    print("getting this url: ", youtube_url)
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    
    print(f"🎥 Analyzing video at {interval}-minute intervals...")
    print("This might take a moment while Gemini watches your video...\n")
    
    try:
        timestamper = VideoTimestamper()
        timestamps = timestamper.generate_timestamps(youtube_url, interval)
        
        if timestamps:
            # Generate filename from video ID
            video_id = youtube_url.split("v=")[-1].split("&")[0]
            output_file = f"timestamps_{video_id}.txt"
            
            formatted = timestamper.format_output(timestamps, output_file)
            print(formatted)
        else:
            print("❌ Failed to generate timestamps")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
