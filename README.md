# Claude.md
claude code jb

## fetch_transcript.py

Fetch the transcript of a YouTube video from the command line.

### Install

```bash
pip install -r requirements.txt
# or: pip install youtube-transcript-api
```

### Usage

```bash
python3 fetch_transcript.py <video-url-or-id> [options]
```

Accepts a bare 11-character video ID or any common YouTube URL
(`watch?v=`, `youtu.be/`, `/shorts/`, `/embed/`, `/live/`).

| Option | Description |
| --- | --- |
| `--languages LANG [LANG ...]` | Preferred language codes in priority order (default: `en`) |
| `-f, --format {text,json,srt,vtt}` | Output format (default: `text`) |
| `--timestamps` | Prefix each line with `[HH:MM:SS]` (text format only) |
| `-o, --output FILE` | Write to a file instead of stdout |
| `--list` | List available transcripts and exit |

### Examples

```bash
python3 fetch_transcript.py dQw4w9WgXcQ
python3 fetch_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
python3 fetch_transcript.py dQw4w9WgXcQ --timestamps
python3 fetch_transcript.py dQw4w9WgXcQ --format srt -o transcript.srt
python3 fetch_transcript.py dQw4w9WgXcQ --languages en de --list
```

> Fetching a transcript requires outbound network access to `youtube.com`.
> In sandboxed environments where that host is blocked, the script will
> report a proxy/connection error.
