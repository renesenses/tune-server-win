# Tune Server — Windows

A multi-room music server for local libraries and streaming services, with DLNA/UPnP, AirPlay, and local audio output.

## Features

- **Library Management** — Scan local music folders, extract metadata, full-text search, browse by directory
- **Multiple Outputs** — DLNA/UPnP renderers, AirPlay devices, local soundcard
- **Multi-Room** — Group zones for synchronized playback
- **Streaming Services** — Tidal, Qobuz, YouTube Music, Amazon Music, Spotify, Deezer
- **Bit-Perfect Playback** — Passthrough when the output supports the source format
- **Native DSD** — DSF/DFF passthrough to DSD-capable DLNA renderers
- **Gapless Playback** — Seamless track transitions with pre-buffering
- **Web Client** — Embedded Svelte SPA served from the same port as the API

## Requirements

- **Windows 10/11** (64-bit)
- **Python 3.11+**
- **FFmpeg**

## Installation

### Option 1: Quick install (recommended)

1. **Install Python** from [python.org](https://www.python.org/downloads/) — check "Add to PATH" during install

2. **Install FFmpeg:**
   ```powershell
   # With winget (Windows 11)
   winget install FFmpeg

   # Or with Chocolatey
   choco install ffmpeg

   # Or manually: download from https://www.gyan.dev/ffmpeg/builds/
   # Extract to C:\ffmpeg and add C:\ffmpeg\bin to PATH
   ```

3. **Install Tune Server:**
   ```powershell
   git clone https://github.com/renesenses/tune-win.git
   cd tune-win
   python -m venv .venv
   .venv\Scripts\activate
   pip install -e .
   ```

4. **Configure:**
   ```powershell
   copy .env.example .env
   # Edit .env — set TUNE_MUSIC_DIRS to your music folder(s)
   ```

5. **Run:**
   ```powershell
   python -m tune_server
   ```

6. Open **http://localhost:8888** in your browser

### Option 2: PyInstaller standalone (no Python needed)

```powershell
# Build (requires Python + PyInstaller)
pip install pyinstaller
pyinstaller --name tune-server --onedir tune_server\__main__.py

# Run
dist\tune-server\tune-server.exe
```

### Option 3: Docker Desktop

```powershell
docker build -t tune-server .
docker run -d --name tune-server ^
    -p 8888:8888 -p 8080:8080 ^
    -v C:\Users\%USERNAME%\Music:/music:ro ^
    -v tune-data:/data ^
    tune-server
```

Note: DLNA/SSDP discovery requires `--network host` which is only available on Docker Desktop with WSL2.

## Configuration

All settings use environment variables with the `TUNE_` prefix. Edit `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `TUNE_MUSIC_DIRS` | `["~/Music"]` | Music folders (JSON array, e.g. `["C:/Users/JP/Music"]`) |
| `TUNE_API_PORT` | `8888` | Web UI + API port |
| `TUNE_STREAM_PORT` | `8080` | Audio streaming port (DLNA) |
| `TUNE_FFMPEG_PATH` | `ffmpeg` | Path to ffmpeg.exe |
| `TUNE_WEB_DIR` | `None` | Path to web UI (auto-detected) |
| `TUNE_LOG_LEVEL` | `INFO` | Log level |

See `.env.example` for all options (streaming services, discovery, etc.).

### Music directories — Windows paths

Use forward slashes or escaped backslashes in `.env`:

```env
TUNE_MUSIC_DIRS=["C:/Users/JP/Music", "D:/FLAC"]
```

## Auto-start with Windows

### Task Scheduler (GUI)

1. Open **Task Scheduler** (`taskschd.msc`)
2. Create Basic Task → "Tune Server"
3. Trigger: "When I log on"
4. Action: Start a program
   - Program: `C:\path\to\tune-win\.venv\Scripts\pythonw.exe`
   - Arguments: `-m tune_server`
   - Start in: `C:\path\to\tune-win`

### PowerShell (one-liner)

```powershell
$action = New-ScheduledTaskAction -Execute "$PWD\.venv\Scripts\pythonw.exe" -Argument "-m tune_server" -WorkingDirectory "$PWD"
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "TuneServer" -Action $action -Trigger $trigger -Description "Tune music server"
```

## Firewall

Windows Firewall will prompt on first launch. Allow access on **private networks** for ports 8888 and 8080. Or manually:

```powershell
netsh advfirewall firewall add rule name="Tune Server API" dir=in action=allow protocol=tcp localport=8888
netsh advfirewall firewall add rule name="Tune Server Stream" dir=in action=allow protocol=tcp localport=8080
```

## Troubleshooting

### "python" is not recognized
→ Reinstall Python and check **"Add Python to PATH"**

### FFmpeg not found
→ Verify: `ffmpeg -version`. If not found, add FFmpeg's `bin` folder to your PATH or set `TUNE_FFMPEG_PATH=C:/ffmpeg/bin/ffmpeg.exe` in `.env`

### No audio devices found
→ Install PortAudio: `pip install sounddevice` should bundle it on Windows. Check `python -c "import sounddevice; print(sounddevice.query_devices())"`

### DLNA devices not discovered
→ Enable SSDP Discovery service: `services.msc` → "SSDP Discovery" → Start + Automatic

### Access from other devices on the network
→ Open http://YOUR_PC_IP:8888 from any browser on the same network. Find your IP with `ipconfig`.

## Updating

```powershell
cd tune-win
git pull
.venv\Scripts\activate
pip install -e .
# Restart the server
```

## License

Private — All rights reserved.
