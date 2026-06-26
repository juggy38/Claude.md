#!/usr/bin/env python3
"""Fetch the full timed transcript for a YouTube video.

Requires network access to youtube.com (set the environment's egress policy to
allow all domains, then start a fresh session so the policy is applied).

Usage:
    pip install youtube-transcript-api
    python3 fetch_transcript.py [VIDEO_ID]

Defaults to the video from the original request if no ID is given.
"""
import sys

from youtube_transcript_api import YouTubeTranscriptApi

DEFAULT_VIDEO_ID = "PkKXm_mKCCM"


def fmt(seconds: float) -> str:
    total = int(seconds)
    m, s = divmod(total, 60)
    h, m = divmod(m, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"


def main() -> None:
    video_id = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_VIDEO_ID
    api = YouTubeTranscriptApi()
    for seg in api.fetch(video_id):
        print(f"[{fmt(seg.start)}] {seg.text}")


if __name__ == "__main__":
    main()
