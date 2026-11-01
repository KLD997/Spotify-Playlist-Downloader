# Spotify Playlist Downloader

A Python wrapper around [SpotDL](https://spotdl.readthedocs.io/) that reads Spotify playlist, album, or track links and downloads matching audio from YouTube Music. It uses Spotify metadata to tag downloaded files.

> **Important:** This does **not** download Spotify's original audio or bypass Spotify DRM. Matches and available audio quality depend on the source. Use it only for music you have permission to download.

## Features

- Downloads a Spotify playlist, album, or individual track by URL.
- Saves files as `Song Name.m4a` (title-only filenames).
- Uses SpotDL to embed supported metadata, including title, artist, album, release information, track number, and album artwork when available.
- Requests M4A output without a forced bitrate conversion.
- Scans for existing songs and attempts to refresh metadata.

**Limitations:** Two tracks with the same title may collide; the current script does not guarantee collision-safe filenames. `--restrict strict` can simplify filenames beyond removing invalid characters. Source tracks may be incorrectly matched, and M4A output is not necessarily lossless or compatible with every player. The script does not perform audio restoration or normalization.

## Files

Save the companion Python script as `spotify_downloader.py` in a convenient folder. The instructions below assume that name. The README does not include the Python script itself.

## Windows

1. Install Python 3 from [python.org](https://www.python.org/downloads/windows/) and enable **Add Python to PATH** during installation (or use the Python launcher `py`).
2. Open **PowerShell** and check:

   ```powershell
   py --version
   ```

3. Install SpotDL and its dependencies:

   ```powershell
   py -m pip install --upgrade spotdl
   py -m spotdl --download-ffmpeg
   py -m spotdl --download-deno
   ```

4. Navigate to the directory containing the script and run it:

   ```powershell
   cd "$HOME\Downloads"
   py .\spotify_downloader.py
   ```

5. Paste your Spotify playlist, album, or track URL when prompted. Press **Enter** to accept the default destination, `Music\Spotify Downloads`, or type a custom path.

If `py` is not found, try `python` in its place. If pip reports an *externally managed environment* or permissions issue, use a virtual environment as described below.

## Linux

1. Install Python 3, pip, FFmpeg, and Deno (if available from your distribution's packages). Example for Debian/Ubuntu:

   ```bash
   sudo apt update
   sudo apt install python3 python3-venv python3-pip ffmpeg
   ```

2. Create a virtual environment and install SpotDL:

   ```bash
   python3 -m venv ~/.venvs/spotdl
   ~/.venvs/spotdl/bin/python -m pip install --upgrade pip spotdl
   ~/.venvs/spotdl/bin/python -m spotdl --download-deno
   ```

   If the Deno helper command is unsupported by your installed SpotDL version, consult its current installation documentation. You may instead install Deno from its official distribution instructions.

3. Run the script:

   ```bash
   ~/.venvs/spotdl/bin/python spotify_downloader.py
   ```

4. Paste the Spotify URL and select a destination. The default is `~/Music/Spotify Downloads`.

**Other distributions:** Use your package manager to install Python 3 and FFmpeg; then follow the same virtual-environment commands.

## FreeBSD (including GhostBSD)

1. Install Python, FFmpeg, and pip support:

   ```sh
   sudo pkg update
   sudo pkg install python3 py311-pip ffmpeg
   ```

   **Package names vary by FreeBSD release.** If `py311-pip` is unavailable or your installed `python3` is a different version, find the matching pip package with `pkg search 'py*-pip'`, or use `python3 -m ensurepip` where supported. Verify with `python3 -m pip --version`.

2. Create a virtual environment:

   ```sh
   python3 -m venv "$HOME/.venvs/spotdl"
   "$HOME/.venvs/spotdl/bin/python" -m pip install --upgrade pip spotdl
   ```

3. Confirm FFmpeg is installed:

   ```sh
   ffmpeg -version
   ```

4. SpotDL's YouTube backend may require Deno. If `deno` is available through your package repository, install it with `sudo pkg install deno`. Otherwise consult the current SpotDL and Deno documentation for supported FreeBSD installation options. Do not assume `spotdl --download-deno` works on every FreeBSD architecture/version.

5. Run:

   ```sh
   "$HOME/.venvs/spotdl/bin/python" spotify_downloader.py
   ```

The default output is `~/Music/Spotify Downloads`.

## How to get a Spotify playlist URL

In Spotify, open the playlist, select **Share**, and choose **Copy link to playlist**. Paste that link into the program. The script also accepts Spotify album and individual track URLs.

## Example session

```text
SPOTIFY MUSIC LIBRARY DOWNLOADER
====================================

Spotify playlist URL: https://open.spotify.com/playlist/EXAMPLEID
Download directory [/home/user/Music/Spotify Downloads]:

Configuration:
Format: M4A
Filename: Song Name.m4a
Metadata: Spotify
Album art: Embedded
Duplicates: Existing files checked
Destination: /home/user/Music/Spotify Downloads
```

`EXAMPLEID` is a placeholder; use a real Spotify link.

## Check metadata and cover art

Use a music player or tag editor (for example, MusicBrainz Picard, Kid3, or Mp3tag) to inspect the resulting files. You can also inspect tags with FFprobe:

```sh
ffprobe -v error -show_entries format_tags -of default=noprint_wrappers=1 "Song Name.m4a"
```

Cover art is embedded only when SpotDL successfully retrieves it. SpotDL's metadata support is not a guarantee that every field exists for every track.

## Troubleshooting

| Problem | What to try |
| --- | --- |
| `No module named spotdl` | Install SpotDL using the **same Python interpreter** that runs the script. |
| `ffmpeg not found` | Install FFmpeg and ensure `ffmpeg` is on your `PATH`. |
| YouTube extraction errors | Update SpotDL and its dependencies; check whether Deno is required by your installed version. |
| Some songs are missing | Check the downloader's error output; tracks can be unavailable or incorrectly matched. |
| Cover art or artist tags are missing | Inspect with a tag editor and verify that Spotify metadata was available. |
| Same-title songs overwrite one another | Use a unique filename template (e.g. `{artists} - {title}.{output-ext}`) or add a collision-safe renaming step. |
| M4A won't play on an older device | Confirm the actual codec with `ffprobe`; re-encode only if needed for device compatibility. |
| `--scan-for-songs` or other flag is rejected | Run `python -m spotdl download --help`; CLI flags may change between SpotDL versions. |

## Updating

Use the same Python environment as installation:

```sh
python -m pip install --upgrade spotdl
```

On Windows, `py -m pip install --upgrade spotdl` is usually appropriate. On Linux and FreeBSD, use the Python executable inside `~/.venvs/spotdl`.

## Notes on audio quality

- The `--format m4a --bitrate disable` options avoid requesting a specific bitrate, but do **not** guarantee that no conversion happens.
- Renaming or converting lossy audio to FLAC does not make it lossless.
- Source quality and licensing are independent of Spotify's playlist metadata.

## References

- [SpotDL documentation](https://spotdl.readthedocs.io/)
- [SpotDL GitHub repository](https://github.com/spotDL/spotify-downloader)
- [FFmpeg](https://ffmpeg.org/)
- [Python](https://www.python.org/)
