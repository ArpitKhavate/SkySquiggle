# SkySquiggle - AI-Powered Air Canvas

Draw in the air with your finger. Press **G** and let AI guess what you drew — out loud.

Built with Python, OpenCV, MediaPipe, Gemini 2.0 Flash, and ElevenLabs TTS.

---

## Features

- **Hand Tracking** — Real-time 21-landmark detection via MediaPipe.
- **Drawing Mode** — Raise only your index finger to draw.
- **Hover / Select Mode** — Raise index + middle finger to navigate without drawing.
- **Colour Palette** — Six virtual buttons at the top of the screen (Red, Blue, Green, Yellow, White, Clear).
- **AI Guess (G key)** — Speaks a filler phrase, sends your drawing to Gemini Vision, then speaks a witty guess.
- **Save (S key)** — Exports your canvas as a timestamped `.png`.
- **Redesigned HUD** — Semi-transparent pill-shaped status indicators at the bottom; pulsing "AI is Thinking..." overlay; fade-in guess banner.

---

## Prerequisites

- Python 3.10+
- Webcam
- Free API keys:
  - [Google AI Studio](https://aistudio.google.com/apikey) (Gemini)
  - [ElevenLabs](https://elevenlabs.io/) (TTS)

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up API keys

Copy the example environment file and fill in your keys:

```bash
cp .env.example .env
```

Then edit `.env`:

```
GEMINI_API_KEY=your_actual_gemini_key
ELEVENLABS_API_KEY=your_actual_elevenlabs_key
```

### 3. Run

```bash
python sky_squiggle.py
```

The hand-landmarker model will auto-download on first run.

---

## Controls

| Input | Action |
|---|---|
| Index finger only | Draw on canvas |
| Index + Middle finger | Hover / Select (no drawing) |
| Hover over colour button (0.5 s) | Change brush colour |
| **G** | AI guess — filler phrase, then Gemini analysis spoken aloud |
| **S** | Save canvas as PNG |
| **Q** | Quit |

---

## How the AI Guess Works

1. Press **G** to trigger a guess.
2. A random filler phrase plays immediately via ElevenLabs ("Hmm, let me see...").
3. While filler plays, the canvas is sent to **Gemini 2.0 Flash** in a background thread.
4. Gemini returns a witty guess (under 10 words).
5. The guess is spoken aloud and displayed as a banner on screen for 5 seconds.
6. The webcam feed never freezes — everything runs on a daemon thread.

---

## Project Structure

```
AirCanvas/
├── sky_squiggle.py        # Main application
├── requirements.txt       # Python dependencies
├── .env.example           # Template for API keys
├── .env                   # Your actual keys (git-ignored)
├── .gitignore             # Excludes .env, models, generated images
├── hand_landmarker.task   # MediaPipe model (auto-downloaded)
├── README.md              # This file
└── LICENSE                # MIT License
```

---

## Configuration

### Hand detection sensitivity

In `sky_squiggle.py`, adjust the `HandLandmarkerOptions`:

```python
min_hand_detection_confidence=0.7   # 0.5–0.9
min_tracking_confidence=0.7         # 0.5–0.9
```

### Brush size

```python
self.brush_thickness = 5   # 1–15
```

### AI models

```python
GEMINI_MODEL = "gemini-2.0-flash"
ELEVENLABS_MODEL_ID = "eleven_flash_v2_5"
ELEVENLABS_VOICE_ID = "lE5ZJB6jGeeuvSNxOvs2"
```

### Guess display duration

```python
GUESS_DISPLAY_SECONDS = 5
```

---

## Troubleshooting

| Issue | Fix |
|---|---|
| Camera not opening | Close other apps; try `cv2.VideoCapture(1)` |
| Hand not detected | Better lighting; lower confidence to 0.5 |
| `GEMINI_API_KEY not found` | Create `.env` from `.env.example` with your key |
| Audio not playing | Ensure `pygame` installed; check speakers |
| Laggy feed | Reduce resolution to 640x480 |

---

## License

MIT — see [LICENSE](LICENSE).
