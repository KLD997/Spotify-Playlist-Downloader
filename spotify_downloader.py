
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_FOLDER = Path.home() / "Music" / "Spotify Downloads"

def valid_spotify_url(url):
    parsed = urlparse(url)
    return (
        parsed.scheme == "https"
        and parsed.hostname in (
            "open.spotify.com",
            "www.open.spotify.com"
        )
        and bool(re.fullmatch(
            r"/(playlist|album|track)/[A-Za-z0-9]+/?",
            parsed.path
        ))
    )

def download(url, destination):
    destination.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable, "-m", "spotdl",
        "download", url,

        # Preserve source quality when possible
        "--format", "m4a",
        "--bitrate", "disable",

        # Song title only
        "--output",
        str(destination / "{title}.{output-ext}"),

        # Sanitize filenames
        "--restrict", "strict",

        # Keep existing audio, refresh metadata
        "--overwrite", "metadata",

        # Look for existing songs
        "--scan-for-songs",

        # Report failed downloads
        "--print-errors",
    ]

    subprocess.run(command, check=True)

def main():
    print("SPOTIFY MUSIC LIBRARY DOWNLOADER")
    print("=" * 36)

    url = input("\nSpotify playlist URL: ").strip()

    if not valid_spotify_url(url):
        print("Invalid Spotify playlist, album, or track URL.")
        return

    folder = input(
        f"Download directory [{DEFAULT_FOLDER}]: "
    ).strip()

    destination = (
        Path(folder).expanduser()
        if folder else DEFAULT_FOLDER
    )

    print("\nConfiguration:")
    print("Format: M4A")
    print("Filename: Song Name.m4a")
    print("Metadata: Spotify")
    print("Album art: Embedded")
    print("Duplicates: Existing files checked")
    print(f"Destination: {destination}")

    try:
        download(url, destination)
        print("\nDownload process finished.")
    except subprocess.CalledProcessError as exc:
        print(f"\nDownload failed: {exc}")
    except KeyboardInterrupt:
        print("\nCancelled by user.")

if __name__ == "__main__":
    main()

