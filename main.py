#!/usr/bin/env python3
"""Show metadata for a video file using ffprobe.

ffprobe (part of ffmpeg) must be installed; the tool checks for it and
reports clearly if it is missing.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys


def parse_args():
    p = argparse.ArgumentParser(
        description="Show metadata for a video file using ffprobe.")
    p.add_argument("file", nargs="?", help="Video file to inspect.")
    p.add_argument("--json", action="store_true",
                   help="Print the raw ffprobe JSON instead of a summary.")
    return p.parse_args()


def probe(path):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
           "-show_format", "-show_streams", path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: ffprobe could not read {path!r}. "
              "Is it a valid media file?", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def fmt_seconds(value):
    try:
        total = float(value)
    except (TypeError, ValueError):
        return "unknown"
    minutes, seconds = divmod(total, 60)
    return f"{int(minutes)}m {seconds:.1f}s"


def fmt_size(value):
    try:
        size = int(value)
    except (TypeError, ValueError):
        return "unknown"
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def show_summary(path, data):
    fmt = data.get("format", {})
    print(f"File: {path}")
    print(f"Format: {fmt.get('format_long_name', 'unknown')}")
    print(f"Duration: {fmt_seconds(fmt.get('duration'))}")
    print(f"Size: {fmt_size(fmt.get('size'))}")
    print(f"Bitrate: {fmt.get('bit_rate', 'unknown')} bps")
    for stream in data.get("streams", []):
        kind = stream.get("codec_type", "?")
        codec = stream.get("codec_name", "unknown")
        if kind == "video":
            print(f"Video: {codec} {stream.get('width')}x"
                  f"{stream.get('height')} "
                  f"@ {stream.get('r_frame_rate', '?')} fps")
        elif kind == "audio":
            print(f"Audio: {codec} {stream.get('sample_rate', '?')} Hz, "
                  f"{stream.get('channels', '?')} channel(s)")
        else:
            print(f"{kind.capitalize()}: {codec}")


def main():
    args = parse_args()
    if shutil.which("ffprobe") is None:
        print("Error: ffprobe is not installed or not on your PATH.\n"
              "It comes with ffmpeg -- install it first, e.g.:\n"
              "  sudo apt install ffmpeg\n"
              "On macOS: brew install ffmpeg", file=sys.stderr)
        sys.exit(1)
    if not args.file:
        print("Error: give a video file to inspect, e.g.\n"
              "  python3 main.py sample.mp4", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(args.file):
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    data = probe(args.file)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        show_summary(args.file, data)


if __name__ == "__main__":
    main()
