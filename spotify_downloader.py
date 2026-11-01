
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

def main():
    print("Spotify Playlist Downloader")
    print("---------------------------")

    url = input("Spotify playlist URL: ").strip()
    parsed = urlparse(url)

    if (
        parsed.hostname not in ("open.spotify.com", "www.open.spotify.com")
        or not parsed.path.startswith("/playlist/")
    ):
        print("Please provide a valid Spotify playlist URL.")
        return

    default = Path.home() / "Music" / "Spotify Downloads"
    folder = input(f"Destination [{default}]: ").strip()
    destination = Path(folder).expanduser() if folder else default
    destination.mkdir(parents=True, exist_ok=True)

    print("\nDownloading available tracks...")
    print(f"Destination: {destination}\n")

    command = [
        sys.executable, "-m", "spotdl",
        "download", url,
        "--format", "m4a",
        "--bitrate", "disable",
        "--output", str(destination / "{artists} - {title}.{output-ext}"),
    ]

    try:
        subprocess.run(command, check=True)
        print("\nDownload completed.")
    except subprocess.CalledProcessError as exc:
        print(f"\nDownload process failed (exit code {exc.returncode}).")
    except KeyboardInterrupt:
        print("\nDownload interrupted.")

if __name__ == "__main__":
    main()
