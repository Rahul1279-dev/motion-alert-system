# Motion Detection Alert System

A real-time motion detection application that monitors a camera feed, detects moving objects, captures images of detected motion, and automatically sends email alerts with the captured images.

---

## How It Works

The system continuously reads frames from a connected camera and compares each frame against a stored reference (the first frame captured at startup). When a significant difference is detected — indicating movement — it draws a bounding box around the moving object and saves a snapshot. Once the motion stops (the status transitions from detected → not detected), an email alert is dispatched in a background thread with one of the captured images attached.

A cleanup routine then deletes all saved snapshots to keep the `Images/` folder tidy for the next detection cycle.

---

## Project Structure

```
.
├── main.py          # Core motion detection loop
├── emailing.py      # Email alert logic
├── steps.png        # Reference/demo image
├── .gitignore       # Excludes .env, IDE files, and __pycache__
└── Images/          # Auto-created folder for captured snapshots (temporary)
```

---

## Requirements

**Python 3.x** and the following packages:

```
opencv-python
Pillow
python-dotenv
```

Install dependencies with:

```bash
pip install opencv-python Pillow python-dotenv
```

---

## Configuration

Create a `.env` file in the project root with your Gmail credentials:

```env
MY_GMAIL_PASSWORD=your_gmail_app_password
SENDER_MAIL=your_email@gmail.com
RECEIVER_MAIL=recipient_email@gmail.com
```

> **Note:** Use a [Gmail App Password](https://support.google.com/accounts/answer/185833), not your regular account password. App Passwords can be generated from your Google Account security settings when 2-Step Verification is enabled.

---

## Usage

```bash
python main.py
```

- A window titled **"Video"** opens showing the live camera feed.
- A second window titled **"My video"** shows the processed (threshold) frame used for motion detection.
- When motion is detected, green bounding boxes appear around moving objects and snapshots are saved to the `Images/` folder.
- When the motion stops, an email alert is automatically sent with a captured image attached.
- Press **`q`** to quit the application.

---

## Camera Setup

In `main.py`, the camera index is set on this line:

```python
video = cv2.VideoCapture(0)
```

| Value | Camera |
|-------|--------|
| `0`   | Built-in laptop/webcam |
| `1`   | External USB camera or third-party camera app |

---

## Key Parameters

| Parameter | Location | Default | Description |
|-----------|----------|---------|-------------|
| Contour area threshold | `main.py` | `5000` px | Minimum pixel area to register as a detected object (filters out noise) |
| Gaussian blur kernel | `main.py` | `(23, 21)` | Smoothing kernel applied before frame differencing |
| Threshold value | `main.py` | `60` | Pixel intensity difference required to flag motion |

---

## Notes

- The first frame captured at startup is used as the static background reference. Make sure the scene is empty and still when you start the script.
- Emails are sent only on the **trailing edge** of detection (motion stops), not on every frame, to avoid alert flooding.
- The `Images/` folder is cleaned up automatically after each detection event.
- The `.env` file is excluded from version control via `.gitignore` — never commit credentials to source control.
