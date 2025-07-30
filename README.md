# Video Timestamper

Extract witty timestamps from long YouTube videos using Gemini API.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Gemini API key:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get your API key from: https://aistudio.google.com/apikey

## Usage

### Command Line
```bash
# Default 30-minute intervals
python video_timestamper.py https://youtube.com/watch?v=YOUR_VIDEO_ID

# Custom interval (e.g., every 20 minutes)
python video_timestamper.py https://youtube.com/watch?v=YOUR_VIDEO_ID 20
```

### Python Script
```python
from video_timestamper import VideoTimestamper

# Initialize
timestamper = VideoTimestamper(api_key="your-key")  # or use env var

# Generate timestamps
timestamps = timestamper.generate_timestamps(
    "https://youtube.com/watch?v=YOUR_VIDEO_ID",
    interval_minutes=30
)

# Display formatted output
formatted = timestamper.format_output(timestamps, save_to_file="output.txt")
print(formatted)
```

## Example Output

```
🎬 Video Timestamps
==================================================

00:00:00 - Host confidently explains something they clearly googled five minutes ago
00:30:00 - The inevitable technical difficulties become part of the show
01:00:00 - Guest arrives fashionably late, blames timezone math
01:30:00 - Deep philosophical tangent about why printers hate us all
02:00:00 - Wrap up includes twelve "one more things" nobody asked for

==================================================
Generated on 2025-01-30 14:32:15
```

## Output Files

The script generates two files:
- `timestamps_VIDEO_ID.txt` - Human-readable format
- `timestamps_VIDEO_ID.json` - JSON format for programmatic use

## Notes

- Works with public YouTube videos only
- 2-hour videos fit within Gemini's context window
- Adjust temperature in code for more/less humor
- Each description is 8-15 words with slight humor