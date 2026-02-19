"""
System Check for SkySquiggle
Verifies that your system is ready to run the application.
"""

import sys
import subprocess
import os


def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_python_version():
    print_section("Python Version Check")
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 10:
        print("PASS - Python 3.10+")
        return True
    elif version.major == 3 and version.minor >= 7:
        print("WARN - Acceptable but 3.10+ recommended")
        return True
    else:
        print("FAIL - Please upgrade to Python 3.10+")
        return False


def check_dependencies():
    print_section("Dependency Check")

    packages = {
        "cv2": "opencv-python",
        "mediapipe": "mediapipe",
        "numpy": "numpy",
        "google.generativeai": "google-generativeai",
        "elevenlabs": "elevenlabs",
        "pygame": "pygame",
        "dotenv": "python-dotenv",
        "PIL": "Pillow",
    }

    all_ok = True
    for module_name, package_name in packages.items():
        try:
            __import__(module_name)
            print(f"  PASS  {package_name}")
        except ImportError:
            print(f"  FAIL  {package_name}  -- NOT INSTALLED")
            all_ok = False
    return all_ok


def check_env_file():
    print_section("Environment File Check")
    if os.path.exists(".env"):
        print("  PASS  .env file found")
        return True
    elif os.path.exists(".env.example"):
        print("  FAIL  .env not found (but .env.example exists)")
        print("        Copy it:  cp .env.example .env")
        return False
    else:
        print("  FAIL  Neither .env nor .env.example found")
        return False


def check_camera():
    print_section("Camera Check")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("  FAIL  Cannot access camera (index 0)")
            return False
        ret, frame = cap.read()
        cap.release()
        if not ret:
            print("  FAIL  Camera opened but cannot read frames")
            return False
        h, w = frame.shape[:2]
        print(f"  PASS  Camera accessible ({w}x{h})")
        return True
    except Exception as e:
        print(f"  FAIL  {e}")
        return False


def test_mediapipe():
    print_section("MediaPipe Hand Detection Test")
    try:
        import mediapipe as mp_lib
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision
        import numpy as np
        import urllib.request

        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "hand_landmarker.task")
        model_url = ("https://storage.googleapis.com/mediapipe-models/"
                     "hand_landmarker/hand_landmarker/float16/latest/"
                     "hand_landmarker.task")
        if not os.path.exists(model_path):
            print("  Downloading hand_landmarker model ...")
            urllib.request.urlretrieve(model_url, model_path)

        base_options = mp_python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=1,
            min_hand_detection_confidence=0.7,
        )
        landmarker = vision.HandLandmarker.create_from_options(options)

        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        mp_image = mp_lib.Image(image_format=mp_lib.ImageFormat.SRGB, data=test_image)
        landmarker.detect(mp_image)
        landmarker.close()
        print("  PASS  MediaPipe HandLandmarker works (Tasks API)")
        return True
    except Exception as e:
        print(f"  FAIL  {e}")
        return False


def display_system_info():
    print_section("System Information")
    import platform
    print(f"  OS       : {platform.system()} {platform.release()}")
    print(f"  Platform : {platform.platform()}")
    print(f"  Processor: {platform.processor()}")


def main():
    print("\n" + "=" * 60)
    print("  SkySquiggle - System Check")
    print("=" * 60)

    checks = []
    checks.append(("Python Version", check_python_version()))
    checks.append(("Dependencies", check_dependencies()))

    if not checks[-1][1]:
        print("\nInstall missing packages:  pip install -r requirements.txt")

    checks.append(("Environment File", check_env_file()))
    checks.append(("Camera", check_camera()))
    checks.append(("MediaPipe", test_mediapipe()))

    display_system_info()

    print_section("Summary")
    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    print(f"\n  {passed}/{total} checks passed\n")
    for name, ok in checks:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}]  {name}")

    print()
    if passed == total:
        print("  All checks passed!  Run:  python sky_squiggle.py")
    else:
        print("  Fix the failures above, then re-run this script.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
