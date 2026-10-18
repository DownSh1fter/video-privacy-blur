# Project plan

## 1. Problem statement

Given a video file or live webcam stream, detect visible human faces and vehicle license plates, then blur each detected region. The output is an anonymized preview or video file.

**Input:** RGB/BGR video frames.

**Output:** same-size frames with expanded sensitive-region boxes blurred; optionally an encoded output video.

**Out of scope:** identity recognition, plate-text recognition, automatic decisions about people, cloud processing, and automatic deletion of the source file.

## 2. System stages

### Stage A — baseline

The first runnable baseline uses OpenCV's pretrained Haar cascade classifiers for frontal faces and Russian-style license plates. A Haar cascade is a traditional feature-based classifier; it is much lighter than a modern neural detector but can miss side profiles, small objects, and plates from other regions. Run it on a short clip, expand its boxes by a configurable margin, and apply Gaussian blur. A diagnostic frame with boxes helps separate detector misses from insufficient coverage or blur. The next baseline will replace the cascades with a modern pretrained detector before fine-tuning.

### Stage B — plate fine-tuning

Choose a public dataset whose license permits the intended use. Keep attribution and the exact dataset version. Fine-tune a pretrained object detector on plate boxes. We will not train a large visual model from random initialization; transfer learning is more practical for a small learning project.

### Stage C — comparison

Run baseline and fine-tuned models on identical validation and test videos. Change one variable at a time (model, image size, or confidence threshold). Preserve the baseline results so an apparent improvement can be checked against the same data.

### Stage D — interface and live performance

The first interface supports local video upload, anonymized preview, output download, and processing statistics. Add live webcam input after validating the video pipeline. Measure throughput and latency on the user's CPU/GPU. Real-time performance depends on frame resolution, selected model, and hardware.

## 3. Data protocol

- Store source videos outside version control unless they are explicitly redistributable and small enough to include.
- Extract labeled frames for training; annotations are bounding boxes around complete visible faces or plates.
- Split by source video or capture session before extracting frames. Never randomly split neighboring frames from one clip across train and test.
- Keep the test set untouched during model selection.
- Record dataset provenance, license, download date, annotation format, class mapping, and split manifest.

## 4. Metrics and interpretation

- **Precision:** of all predicted sensitive regions, what fraction were correct? Low precision means extra areas are blurred.
- **Recall:** of all labeled sensitive regions, what fraction did the model detect? Low recall means some faces or plates remain visible.
- **mAP@0.5:** average detection quality over classes using a box-overlap threshold of 0.5. It summarizes localization and ranking, but does not replace class-level recall for privacy.
- **FPS:** processed frames per second. Compare against the source video's frame rate.
- **Latency:** time to process a frame (or a defined batch), in milliseconds.
- **False negative review:** manually inspect misses, especially small and partially hidden objects.

Confidence thresholds are selected using validation data. For privacy, we may choose a lower threshold if it materially improves recall and the additional false positives are acceptable. The final threshold and trade-off must be reported.

## 5. Reproducibility

Each experiment records:

- experiment ID and date;
- code revision;
- detector architecture and checkpoint source;
- dataset version, license, and split manifest hash;
- image size, batch size, confidence/IoU settings, and blur margin;
- training hyperparameters, random seed, and hardware;
- precision, recall, mAP@0.5, FPS, and latency;
- known errors and visual examples.

## 6. Risks to quality

A model trained on one country, camera, or lighting setup may generalize poorly to another. License-plate shape and language vary. Faces and plates can be tiny or occluded. A blur box that is too tight can leave readable edges; one that is too large can hide useful context. These issues will be documented and measured rather than hidden behind a single score.
