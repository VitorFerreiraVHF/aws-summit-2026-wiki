from __future__ import annotations

import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
INCOMING = ROOT / "_work" / "incoming" / "Aws Summit 2026 midias"
REPORTS = ROOT / "_work" / "reports"
ASSETS = ROOT / "04-midias-e-evidencias" / "assets"
PHOTOS = ASSETS / "fotos"
VIDEOS = ASSETS / "videos"
AUDIO = ASSETS / "audio"
MODELS = ROOT / "_work" / "models"

FFMPEG = (
    Path(sys.executable).parent
    / "Lib"
    / "site-packages"
    / "imageio_ffmpeg"
    / "binaries"
    / "ffmpeg-win-x86_64-v7.1.exe"
)

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v"}
AUDIO_EXTS = {".m4a", ".mp3", ".wav", ".aac", ".mpeg"}


@dataclass
class MediaItem:
    id: str
    type: str
    original_name: str
    source_path: str
    output_path: str
    relative_output_path: str
    size_bytes: int
    width: int | None = None
    height: int | None = None
    duration_seconds: float | None = None
    faces_detected: int | None = None
    notes: str = ""


def ensure_dirs() -> None:
    for directory in [REPORTS, PHOTOS, VIDEOS, AUDIO, MODELS]:
        directory.mkdir(parents=True, exist_ok=True)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "arquivo"


def read_image(path: Path) -> np.ndarray:
    image = Image.open(path)
    image = ImageOps.exif_transpose(image).convert("RGB")
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def write_image(path: Path, image_bgr: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(path, quality=92, optimize=True)


def download_yunet() -> Path | None:
    model_path = MODELS / "face_detection_yunet_2023mar.onnx"
    if model_path.exists() and model_path.stat().st_size > 0:
        return model_path

    url = "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
    try:
        urllib.request.urlretrieve(url, model_path)
        return model_path
    except Exception as exc:
        print(f"warning: could not download YuNet model, falling back to Haar only: {exc}")
        return None


def load_detectors():
    yunet = None
    model_path = download_yunet()
    if model_path is not None and hasattr(cv2, "FaceDetectorYN_create"):
        try:
            yunet = cv2.FaceDetectorYN_create(
                str(model_path),
                "",
                (320, 320),
                score_threshold=0.55,
                nms_threshold=0.3,
                top_k=5000,
            )
        except Exception as exc:
            print(f"warning: YuNet unavailable, using Haar only: {exc}")
            yunet = None

    haar_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_alt2.xml"
    haar = cv2.CascadeClassifier(str(haar_path))
    return yunet, haar


def expand_box(x: int, y: int, w: int, h: int, width: int, height: int, factor: float = 0.35):
    pad_x = int(w * factor)
    pad_y = int(h * factor)
    x1 = max(0, x - pad_x)
    y1 = max(0, y - pad_y)
    x2 = min(width, x + w + pad_x)
    y2 = min(height, y + h + pad_y)
    return x1, y1, x2, y2


def iou(a, b) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    inter_x1, inter_y1 = max(ax1, bx1), max(ay1, by1)
    inter_x2, inter_y2 = min(ax2, bx2), min(ay2, by2)
    inter = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
    if inter == 0:
        return 0.0
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    return inter / float(area_a + area_b - inter)


def dedupe_boxes(boxes):
    deduped = []
    for box in sorted(boxes, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]), reverse=True):
        if all(iou(box, existing) < 0.35 for existing in deduped):
            deduped.append(box)
    return deduped


def detect_faces(image_bgr: np.ndarray, yunet, haar, max_dim: int = 960):
    height, width = image_bgr.shape[:2]
    resize_scale = min(1.0, max_dim / float(max(width, height)))
    if resize_scale < 1.0:
        detect_img = cv2.resize(image_bgr, (int(width * resize_scale), int(height * resize_scale)), interpolation=cv2.INTER_AREA)
    else:
        detect_img = image_bgr
    detect_h, detect_w = detect_img.shape[:2]
    boxes = []

    if yunet is not None:
        try:
            yunet.setInputSize((detect_w, detect_h))
            _, faces = yunet.detect(detect_img)
            if faces is not None:
                for face in faces:
                    x, y, w, h = [int(round(v)) for v in face[:4]]
                    if w > 8 and h > 8:
                        x = int(x / resize_scale)
                        y = int(y / resize_scale)
                        w = int(w / resize_scale)
                        h = int(h / resize_scale)
                        boxes.append(expand_box(x, y, w, h, width, height))
        except Exception:
            pass

    gray = cv2.cvtColor(detect_img, cv2.COLOR_BGR2GRAY)
    min_size = max(24, min(detect_w, detect_h) // 35)
    for haar_scale in [1.05, 1.1]:
        faces = haar.detectMultiScale(
            gray,
            scaleFactor=haar_scale,
            minNeighbors=4,
            minSize=(min_size, min_size),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )
        for x, y, w, h in faces:
            if resize_scale < 1.0:
                x = int(x / resize_scale)
                y = int(y / resize_scale)
                w = int(w / resize_scale)
                h = int(h / resize_scale)
            boxes.append(expand_box(int(x), int(y), int(w), int(h), width, height))

    return dedupe_boxes(boxes)


def blur_faces(image_bgr: np.ndarray, boxes) -> np.ndarray:
    output = image_bgr.copy()
    for x1, y1, x2, y2 in boxes:
        roi = output[y1:y2, x1:x2]
        if roi.size == 0:
            continue
        small_w = max(1, (x2 - x1) // 18)
        small_h = max(1, (y2 - y1) // 18)
        pixelated = cv2.resize(roi, (small_w, small_h), interpolation=cv2.INTER_LINEAR)
        pixelated = cv2.resize(pixelated, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
        blurred = cv2.GaussianBlur(pixelated, (0, 0), sigmaX=18, sigmaY=18)
        output[y1:y2, x1:x2] = blurred
    return output


def get_duration(path: Path) -> float | None:
    if not FFMPEG.exists():
        return None
    command = [str(FFMPEG), "-hide_banner", "-i", str(path)]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", result.stdout)
    if not match:
        return None
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def ffmpeg_copy_audio(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if FFMPEG.exists():
        command = [str(FFMPEG), "-y", "-hide_banner", "-loglevel", "error", "-i", str(source), "-vn", "-c:a", "copy", str(destination)]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0 and destination.exists() and destination.stat().st_size > 0:
            return
    shutil.copy2(source, destination)


def has_audio_stream(source: Path) -> bool:
    if not FFMPEG.exists():
        return False
    command = [str(FFMPEG), "-hide_banner", "-i", str(source)]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    return "Audio:" in result.stdout


def mux_audio(original: Path, silent_video: Path, destination: Path) -> None:
    if not FFMPEG.exists() or not has_audio_stream(original):
        shutil.move(str(silent_video), str(destination))
        return
    command = [
        str(FFMPEG),
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(silent_video),
        "-i",
        str(original),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-shortest",
        str(destination),
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"warning: mux failed for {original.name}: {result.stderr}")
        shutil.move(str(silent_video), str(destination))
    else:
        silent_video.unlink(missing_ok=True)


def process_images(files: list[Path], yunet, haar) -> list[MediaItem]:
    items = []
    for idx, source in enumerate(files, start=1):
        image = read_image(source)
        h, w = image.shape[:2]
        boxes = detect_faces(image, yunet, haar, max_dim=960)
        redacted = blur_faces(image, boxes)
        media_id = f"FOTO-{idx:03d}"
        destination = PHOTOS / f"{media_id}__2026-09-04__aws-summit-2026__censurado.jpg"
        write_image(destination, redacted)
        items.append(
            MediaItem(
                id=media_id,
                type="foto",
                original_name=source.name,
                source_path=str(source),
                output_path=str(destination),
                relative_output_path=destination.relative_to(ROOT).as_posix(),
                size_bytes=source.stat().st_size,
                width=w,
                height=h,
                faces_detected=len(boxes),
                notes="Imagem saneada com deteccao automatica de rostos.",
            )
        )
        print(f"{media_id}: {source.name} -> {len(boxes)} face(s)", flush=True)
    return items


def process_videos(files: list[Path], yunet, haar) -> list[MediaItem]:
    items = []
    for idx, source in enumerate(files, start=1):
        media_id = f"VID-{idx:03d}"
        destination = VIDEOS / f"{media_id}__2026-09-04__aws-summit-2026__censurado.mp4"
        temp_video = VIDEOS / f"{media_id}__temp_silent.mp4"
        cap = cv2.VideoCapture(str(source))
        if not cap.isOpened():
            print(f"warning: could not open video {source}")
            continue
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(temp_video), fourcc, fps, (width, height))
        total_faces = 0
        frame_count = 0
        last_boxes = []
        detect_every = 3
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if frame_count % detect_every == 0:
                last_boxes = detect_faces(frame, yunet, haar, max_dim=640)
            boxes = last_boxes
            total_faces += len(boxes)
            redacted = blur_faces(frame, boxes)
            writer.write(redacted)
            frame_count += 1
        writer.release()
        cap.release()
        mux_audio(source, temp_video, destination)
        items.append(
            MediaItem(
                id=media_id,
                type="video",
                original_name=source.name,
                source_path=str(source),
                output_path=str(destination),
                relative_output_path=destination.relative_to(ROOT).as_posix(),
                size_bytes=source.stat().st_size,
                width=width,
                height=height,
                duration_seconds=get_duration(source),
                faces_detected=total_faces,
                notes=f"Video saneado automaticamente. Frames processados: {frame_count}.",
            )
        )
        print(f"{media_id}: {source.name} -> {total_faces} face detections across {frame_count} frame(s)", flush=True)
    return items


def process_audio(files: list[Path]) -> list[MediaItem]:
    items = []
    for idx, source in enumerate(files, start=1):
        parsed = re.search(r"(\d{2})-(\d{2})-(\d{4})\s+(\d{2})\.(\d{2})", source.name)
        if parsed:
            day, month, year, hour, minute = parsed.groups()
            stamp = f"{year}-{month}-{day}-{hour}{minute}"
        else:
            stamp = f"audio-{idx:03d}"
        media_id = f"AUD-{idx:03d}"
        destination = AUDIO / f"{media_id}__{stamp}__gravacao-palestra.m4a"
        ffmpeg_copy_audio(source, destination)
        items.append(
            MediaItem(
                id=media_id,
                type="audio",
                original_name=source.name,
                source_path=str(source),
                output_path=str(destination),
                relative_output_path=destination.relative_to(ROOT).as_posix(),
                size_bytes=source.stat().st_size,
                duration_seconds=get_duration(source),
                notes="Audio original convertido/copiado para M4A; voz preservada; revisar autorizacao antes de compartilhar.",
            )
        )
        print(f"{media_id}: {source.name}", flush=True)
    return items


def create_contact_sheets(image_items: list[MediaItem]) -> None:
    sheet_dir = REPORTS / "contact-sheets"
    sheet_dir.mkdir(parents=True, exist_ok=True)
    thumb_w, thumb_h = 560, 420
    cols, rows = 3, 3
    margin = 24
    label_h = 54
    font = ImageFont.load_default()
    images_per_sheet = cols * rows

    for sheet_idx in range(math.ceil(len(image_items) / images_per_sheet)):
        batch = image_items[sheet_idx * images_per_sheet : (sheet_idx + 1) * images_per_sheet]
        sheet = Image.new("RGB", (cols * (thumb_w + margin) + margin, rows * (thumb_h + label_h + margin) + margin), "white")
        draw = ImageDraw.Draw(sheet)
        for i, item in enumerate(batch):
            x = margin + (i % cols) * (thumb_w + margin)
            y = margin + (i // cols) * (thumb_h + label_h + margin)
            img = Image.open(ROOT / item.relative_output_path).convert("RGB")
            img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            bg = Image.new("RGB", (thumb_w, thumb_h), (245, 245, 245))
            bg.paste(img, ((thumb_w - img.width) // 2, (thumb_h - img.height) // 2))
            sheet.paste(bg, (x, y + label_h))
            label = f"{item.id} | faces: {item.faces_detected} | {item.original_name}"
            draw.text((x, y), label[:90], fill=(0, 0, 0), font=font)
        output = sheet_dir / f"contact-sheet-{sheet_idx + 1:02d}.jpg"
        sheet.save(output, quality=92)
        print(f"contact sheet: {output}", flush=True)


def write_manifest(items: list[MediaItem]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    json_path = REPORTS / "media_manifest.json"
    json_path.write_text(json.dumps([asdict(item) for item in items], indent=2, ensure_ascii=False), encoding="utf-8")

    csv_path = REPORTS / "media_manifest.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(items[0]).keys()) if items else ["id"])
        writer.writeheader()
        for item in items:
            writer.writerow(asdict(item))


def main() -> int:
    ensure_dirs()
    if not INCOMING.exists():
        print(f"Incoming folder not found: {INCOMING}", file=sys.stderr)
        return 1

    files = sorted([path for path in INCOMING.iterdir() if path.is_file()], key=lambda p: p.name.lower())
    image_files = [p for p in files if p.suffix.lower() in IMAGE_EXTS]
    video_files = [p for p in files if p.suffix.lower() in VIDEO_EXTS]
    audio_files = [p for p in files if p.suffix.lower() in AUDIO_EXTS and p.suffix.lower() not in VIDEO_EXTS]

    yunet, haar = load_detectors()
    all_items: list[MediaItem] = []
    image_items = process_images(image_files, yunet, haar)
    all_items.extend(image_items)
    all_items.extend(process_videos(video_files, yunet, haar))
    all_items.extend(process_audio(audio_files))
    create_contact_sheets(image_items)
    write_manifest(all_items)
    print(f"processed {len(all_items)} media item(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
