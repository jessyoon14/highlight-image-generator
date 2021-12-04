import os

# STORAGE_DIR = "/home/yominx/ws/highlight-image-generator/media"
STORAGE_DIR = "/Users/jessyoon/KAIST/1-intro-to-deep-learning/final-proj/highlight-generator/media"
# STORAGE_DIR = os.environ.get("STORAGE_DIR", "media")
# if not STORAGE_DIR.startswith("/"):
#     STORAGE_DIR = os.path.join("..", STORAGE_DIR)  # We are in local/loader

VIDEO_DIR = f"{STORAGE_DIR}/video"
AUDIO_DIR = f"{STORAGE_DIR}/audio"
AUDIO_RES_DIR = f"{STORAGE_DIR}/audio_result"
IMAGE_RES_DIR = f"{STORAGE_DIR}/image_result"
# VV_DIR = f"/home/yominx/ws/highlight-image-generator/VisualVoice"
VV_DIR = "/Users/jessyoon/KAIST/1-intro-to-deep-learning/final-proj/highlight-generator/VisualVoice"
# CAPTURED_DIR = f"{STORAGE_DIR}/image_captured"