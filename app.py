from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)
CORS(app)

def extract_video_id(url_or_id):
    # Agar already sirf ID hai
    if re.fullmatch(r"[a-zA-Z0-9_-]{11}", url_or_id):
        return url_or_id
    # Common YouTube URL patterns
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|$)",
        r"youtu\.be\/([0-9A-Za-z_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return None

@app.route("/")
def home():
    return jsonify({"status": "YT Transcript Free backend is running"})

@app.route("/get-transcript", methods=["GET"])
def get_transcript():
    url_or_id = request.args.get("video_id", "")
    video_id = extract_video_id(url_or_id)

    if not video_id:
        return jsonify({"error": "Invalid YouTube URL or video ID"}), 400

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([item["text"] for item in transcript_list])
        return jsonify({
            "video_id": video_id,
            "transcript": transcript_list,
            "full_text": full_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
