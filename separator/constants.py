import os

STORAGE_DIR = os.environ.get("STORAGE_DIR", "media")
if not STORAGE_DIR.startswith("/"):
    STORAGE_DIR = os.path.join("..", STORAGE_DIR)  # We are in local/loader


VIDEO_DIR = f"{STORAGE_DIR}/video"
AUDIO_DIR = f"{STORAGE_DIR}/audio"
AUDIO_RES_DIR = f"{STORAGE_DIR}/audio_result"
CAPTURED_DIR = f"{STORAGE_DIR}/image_captured"