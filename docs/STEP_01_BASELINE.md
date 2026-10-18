# Step 1 — the first video baseline

## What is a baseline?

A **baseline** is a simple, reproducible first system. It gives us a reference score and concrete failure cases. A more complex model is useful only if it improves measured quality or speed on the same held-out data.

## What the app does

1. Streamlit receives a short video file from the local browser.
2. The file is placed in a temporary local directory for processing.
3. OpenCV reads the video frame by frame. We do not load a long video fully into memory.
4. Each frame is converted to grayscale. The cascade models use intensity patterns rather than color.
5. `detectMultiScale` scans each frame at several window sizes and returns rectangles for likely frontal faces and Russian-style plates.
6. The rectangle is expanded by 18% in each direction so blur is less likely to leave readable edges.
7. Gaussian blur is applied only inside the expanded rectangles.
8. OpenCV writes the processed frames to MP4. This first version does not copy the original audio track.
9. The app displays a preview and download button. Temporary input/output files are removed after the app reads the processed bytes.

## What is a Haar cascade?

OpenCV's Haar cascade is a traditional machine-learning detector. It was trained earlier on positive examples (images containing the target) and negative examples. Haar-like features measure simple light/dark patterns; boosted stages quickly reject most image windows before later stages examine the remaining candidates. OpenCV describes the feature-based cascade method in its [official tutorial](https://docs.opencv.org/5.0/tutorials_contrib/xobjdetect/cascade_classifier/cascade_classifier.html).

This project loads pretrained XML classifiers supplied with OpenCV; **we are not training a new detector at this step**. The face cascade is intended for mostly frontal faces, and the plate cascade is specialized for Russian-style plate appearance. Both can miss objects in other poses, sizes, regions, or lighting.

## Important parameters in `video.py`

- `scaleFactor=1.1`: change the search-window size by about 10% between scales. Smaller steps can find more sizes but take longer.
- `minNeighbors=5` for faces and `3` for plates: how many nearby candidate rectangles must agree before a detection is kept. Larger values usually reduce false detections and may increase misses.
- `minSize`: ignore windows smaller than a minimum pixel size.
- `margin_ratio=0.18`: enlarge each detection box by 18% before blurring.
- Gaussian kernel size: larger kernels hide detail more strongly but can make output less useful.

These settings are starting values, not optimized results. We will change them only while inspecting examples and recording the effect.

## What we measure next

Try one short video containing known faces and plates. For each class, count labeled objects, detected objects, misses, and extra detections; inspect the boxes and output manually. Record processing FPS and compare it with the source FPS. Do not interpret the first run as reliable anonymization.

After we choose a licensed dataset and modern detector, we will use the same held-out videos to compare precision, recall, and mAP. For privacy, **recall and false-negative review are especially important** because a missed region remains visible.
