# Video Privacy Blur

[Русская версия](README.ru.md)

A local computer-vision application that detects faces and vehicle license plates in a video stream and blurs those regions. The project focuses on privacy-preserving video processing. It does not identify people or read plate text.

## Project status

**Step 0 — task definition and evaluation plan:** documented.

**Step 1 — runnable video baseline:** implemented with OpenCV Haar cascades and Gaussian blur. This is a traditional, lightweight baseline, not the deep detector we plan to fine-tune.

**Next:** run the baseline on a short clip, record its misses, and choose a licensed dataset and modern pretrained detector for fine-tuning.

## What we are building

1. Read frames from an uploaded video file.
2. Detect face and license-plate bounding boxes.
3. Expand each box slightly and blur the region.
4. Preview the result or save an anonymized video.
5. Fine-tune a pretrained detector for license plates and compare it with the baseline.

The local Streamlit app writes the uploaded clip to a temporary local directory, processes it, returns the anonymized MP4, and removes its temporary files. The app does not send frames to a remote service. The baseline output has no audio track.

## Run on Windows

Double-click `start-app.bat`. On the first run it creates a local `.venv`, installs the project dependencies, and opens the app in your browser. Select a short MP4/AVI/MOV/MKV clip and choose **Process video**. Review the result carefully: Haar cascades can miss faces or plates, and the current MP4 output is silent.

To run manually:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -e .
python -m streamlit run src/privacy_blur/app.py
```

## Why this is an ML engineering project

The work covers data sourcing and annotation, transfer learning, train/validation/test design, object-detection metrics, error analysis, inference latency, and an end-to-end video pipeline. We will measure whether the detector finds sensitive regions and whether the processing speed is practical for a live stream.

## Planned milestones

- [x] Define the task, scope, terminology, and evaluation protocol.
- [ ] Select datasets and models; record their licenses and limitations.
- [x] Build a traditional CV baseline that detects and blurs faces and license plates in an uploaded clip.
- [ ] Annotate or prepare license-plate training data and fine-tune a pretrained detector.
- [ ] Compare baseline and fine-tuned models on the same held-out videos.
- [ ] Add a small interface for video upload, webcam input, preview, and output download.
- [ ] Document reproducible setup, experiments, failure cases, and model limitations.

## Evaluation principles

- Split data by source video or capture session, not by adjacent frames. Neighboring frames look nearly identical and can leak information between splits.
- Use the validation set to choose confidence thresholds and settings; reserve the test set for final comparison.
- Report per-class precision and recall, mAP@0.5, inference speed, and representative misses and false detections.
- Prioritize recall for privacy: a missed face or plate remains visible. Also report false positives because excessive blur makes footage less useful.
- Record the model, dataset version, split, image size, threshold, hardware, and random seed for every experiment.

## Scope and limitations

The detector locates a face or a plate; it does not identify a person, perform face recognition, or perform optical character recognition (OCR) on plates. Detection can fail on small, occluded, angled, dark, or motion-blurred objects. The application must show that failures are possible and should be checked before sharing a processed video.

See [the project plan](docs/PROJECT_PLAN.md), [step 1: baseline](docs/STEP_01_BASELINE.md), [data sources](docs/DATA_SOURCES.md), [the glossary](docs/GLOSSARY.md), and [the experiment log](docs/EXPERIMENTS.md) for details.
