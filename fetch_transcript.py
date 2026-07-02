#!/usr/bin/env python3
"""Fetch a transcript for a YouTube video.

Usage:
    python3 fetch_transcript.py <video-url-or-id> [options]

Examples:
    python3 fetch_transcript.py dQw4w9WgXcQ
    python3 fetch_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    python3 fetch_transcript.py dQw4w9WgXcQ --format srt -o out.srt
    python3 fetch_transcript.py dQw4w9WgXcQ --languages en de --timestamps
    python3 fetch_transcript.py dQw4w9WgXcQ --list

Requires:
    pip install youtube-transcript-api
"""

import argparse
import re
import sys
from urllib.parse import parse_qs, urlparse

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import (
        JSONFormatter,
        SRTFormatter,
        TextFormatter,
        WebVTTFormatter,
    )
except ImportError:
    sys.exit(
        "Missing dependency. Install it with:\n"
        "    pip install youtube-transcript-api"
    )


def extract_video_id(value: str) -> str:
    """Accept a raw 11-char video ID or any common YouTube URL form."""
    value = value.strip()

    # Already a bare video ID.
    if re.fullmatch(r"[0-9A-Za-z_-]{11}", value):
        return value

    parsed = urlparse(value)
    host = (parsed.hostname or "").lower().removeprefix("www.")

    if host == "youtu.be":
        candidate = parsed.path.lstrip("/").split("/")[0]
    elif host == "youtube.com" or host.endswith(".youtube.com"):
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [""])[0]
        else:
            # /embed/<id>, /shorts/<id>, /live/<id>, /v/<id>
            parts = [p for p in parsed.path.split("/") if p]
            candidate = parts[-1] if parts else ""
    else:
        candidate = ""

    if re.fullmatch(r"[0-9A-Za-z_-]{11}", candidate):
        return candidate

    sys.exit(f"Could not extract a YouTube video ID from: {value!r}")


def format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube video transcript.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("video", help="YouTube video URL or 11-character video ID")
    parser.add_argument(
        "--languages",
        nargs="+",
        default=["en"],
        metavar="LANG",
        help="Preferred language codes in priority order (default: en)",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["text", "json", "srt", "vtt"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Prefix each line with a [HH:MM:SS] timestamp (text format only)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Write output to FILE instead of stdout",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available transcripts for the video and exit",
    )
    args = parser.parse_args()

    video_id = extract_video_id(args.video)
    ytt_api = YouTubeTranscriptApi()

    if args.list:
        transcript_list = ytt_api.list(video_id)
        print(f"Available transcripts for {video_id}:")
        for t in transcript_list:
            kind = "auto-generated" if t.is_generated else "manual"
            translatable = ", translatable" if t.is_translatable else ""
            print(f"  - {t.language_code} ({t.language}) [{kind}{translatable}]")
        return 0

    fetched = ytt_api.fetch(video_id, languages=args.languages)

    if args.format == "json":
        output = JSONFormatter().format_transcript(fetched, indent=2)
    elif args.format == "srt":
        output = SRTFormatter().format_transcript(fetched)
    elif args.format == "vtt":
        output = WebVTTFormatter().format_transcript(fetched)
    elif args.timestamps:
        output = "\n".join(
            f"[{format_timestamp(s.start)}] {s.text}" for s in fetched
        )
    else:
        output = TextFormatter().format_transcript(fetched)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output + "\n")
        print(f"Wrote transcript to {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - surface a clean message to the CLI user
        sys.exit(f"Error: {exc}")
