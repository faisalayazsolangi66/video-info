# Video Info

Show metadata for a video file (format, duration, size, bitrate, video
and audio streams) using ffprobe.

## Requirements

- Python 3 (standard library only)
- ffprobe installed and on your `PATH` (it ships with ffmpeg) — the tool
  checks for it and exits with a clear message if it is missing. Install
  with e.g. `sudo apt install ffmpeg` (Ubuntu/Debian) or
  `brew install ffmpeg` (macOS).

## How to run

```bash
python3 main.py movie.mp4
python3 main.py movie.mp4 --json
```

Options:

- `--json` — print the raw ffprobe JSON instead of the summary

## Example

```bash
python3 main.py movie.mp4
```

Sample output:

```
File: movie.mp4
Format: QuickTime / MOV
Duration: 8m 10.0s
Size: 59.0 MB
Bitrate: 1000000 bps
Video: h264 1280x720 @ 30/1 fps
Audio: aac 48000 Hz, 2 channel(s)
```

If ffprobe is missing:

```
Error: ffprobe is not installed or not on your PATH.
It comes with ffmpeg -- install it first, e.g.:
  sudo apt install ffmpeg
On macOS: brew install ffmpeg
```

## License

MIT — see [LICENSE](LICENSE).
