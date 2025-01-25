# ViralShortGen

**ViralShortGen** is a Python-based tool for generating YouTube Shorts from trending videos. It intelligently picks the most exciting moments from the videos and learns from user feedback to create short, engaging clips perfect for going viral.

## Features

- Fetches trending YouTube videos based on real-time data.
- Analyzes videos to extract the most exciting moments.
- Generates YouTube Shorts (15-60 seconds).
- Learns from user feedback to improve future video selections.
- Skips previously reviewed video IDs to avoid repetition.
- Supports multiple pages of trending videos to maximize short generation.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Gh0styTongue/ViralShortGen.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the YouTube API:
   - Get your Google API key by following [this guide](https://developers.google.com/youtube/registering_an_application).
   - Add your API key in the `shorts.py` file by setting the `API_KEY` variable.

## Usage

1. Run the script:
   ```bash
   python shorts.py
   ```

2. The script will generate 5 shorts based on trending videos. After the first run, you'll be asked if you want to generate more shorts. Type `yes` to continue, or `no` to stop.

3. The script will learn from your feedback on each short and try to improve future selections.

## Feedback Mechanism

After generating a short, you will be prompted to give feedback:

- Type `yes` if the short is good.
- Type `no` if the short is not good.

The feedback will be saved, and the tool will avoid generating similar shorts in future runs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
