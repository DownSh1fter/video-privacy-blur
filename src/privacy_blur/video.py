"""Video processing helpers for the initial OpenCV Haar-cascade baseline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Callable

import cv2
import numpy as np


@dataclass(frozen=True)
class Detection:
    """A rectangular region and its semantic label."""

    x: int
    y: int
    width: int
    height: int
    label: str


@dataclass(frozen=True)
class VideoStats:
    """Basic throughput statistics for one processed video."""

    frames: int
    source_fps: float
    processing_fps: float
    elapsed_seconds: float


class HaarCascadeDetector:
    """Run OpenCV's pretrained face and Russian license-plate cascades."""

    def __init__(self) -> None:
        cascade_dir = Path(cv2.data.haarcascades)
        self.face = cv2.CascadeClassifier(str(cascade_dir / "haarcascade_frontalface_default.xml"))
        self.plate = cv2.CascadeClassifier(str(cascade_dir / "haarcascade_russian_plate_number.xml"))
        if self.face.empty():
            raise RuntimeError("Could not load OpenCV's frontal-face cascade")
        if self.plate.empty():
            raise RuntimeError("Could not load OpenCV's Russian license-plate cascade")

    def detect(self, frame: np.ndarray) -> list[Detection]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found: list[Detection] = []
        for label, cascade, scale, neighbors, minimum in (
            ("face", self.face, 1.1, 5, (24, 24)),
            ("license_plate", self.plate, 1.08, 3, (40, 16)),
        ):
            boxes = cascade.detectMultiScale(
                gray,
                scaleFactor=scale,
                minNeighbors=neighbors,
                minSize=minimum,
            )
            found.extend(
                Detection(int(x), int(y), int(width), int(height), label)
                for x, y, width, height in boxes
            )
        return found


def blur_regions(
    frame: np.ndarray,
    detections: list[Detection],
    margin_ratio: float = 0.18,
) -> np.ndarray:
    """Blur each detected box with a margin so its edges are covered too."""
    height, width = frame.shape[:2]
    output = frame.copy()
    for detection in detections:
        margin_x = round(detection.width * margin_ratio)
        margin_y = round(detection.height * margin_ratio)
        x1 = max(0, detection.x - margin_x)
        y1 = max(0, detection.y - margin_y)
        x2 = min(width, detection.x + detection.width + margin_x)
        y2 = min(height, detection.y + detection.height + margin_y)
        region = output[y1:y2, x1:x2]
        if region.size == 0:
            continue
        kernel_width = max(15, (region.shape[1] // 5) | 1)
        kernel_height = max(15, (region.shape[0] // 5) | 1)
        output[y1:y2, x1:x2] = cv2.GaussianBlur(
            region,
            (kernel_width, kernel_height),
            sigmaX=0,
        )
    return output


def process_video(
    input_path: Path,
    output_path: Path,
    progress: Callable[[float], None] | None = None,
) -> VideoStats:
    """Detect and blur sensitive regions in every frame of a video.

    OpenCV's VideoWriter does not preserve the input audio track. The output is
    therefore a silent video in this baseline.
    """
    capture = cv2.VideoCapture(str(input_path))
    if not capture.isOpened():
        raise ValueError("Could not open this video file")

    source_fps = float(capture.get(cv2.CAP_PROP_FPS)) or 25.0
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        capture.release()
        raise ValueError("The video has invalid frame dimensions")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        source_fps,
        (width, height),
    )
    if not writer.isOpened():
        capture.release()
        raise RuntimeError("Could not create the output MP4 video")

    detector = HaarCascadeDetector()
    start = perf_counter()
    processed = 0
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            detections = detector.detect(frame)
            writer.write(blur_regions(frame, detections))
            processed += 1
            if progress is not None and frame_count > 0:
                progress(min(processed / frame_count, 1.0))
    finally:
        capture.release()
        writer.release()

    elapsed = perf_counter() - start
    return VideoStats(
        frames=processed,
        source_fps=source_fps,
        processing_fps=processed / elapsed if elapsed > 0 else 0.0,
        elapsed_seconds=elapsed,
    )
