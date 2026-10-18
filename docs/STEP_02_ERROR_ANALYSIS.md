# Step 2: Find out why a region stayed visible

## What we are doing

Before replacing the detector, we need to see what happens inside the pipeline. The app first detects rectangular regions, then blurs only those regions. A readable plate can therefore point to two different failures:

1. **Detector miss (false negative):** there is no box around the plate. Blur strength is irrelevant because the detector did not give the app a region to process.
2. **Insufficient coverage or blur:** a box exists, but it misses part of the plate or the blur still leaves readable detail.

These failures need different fixes. Stronger blur cannot fix a detector miss; a stronger detector cannot fix a box that is too small.

## Inspect your clip

1. Start the app by double-clicking `start-app.bat`.
2. Upload a short clip and find a timestamp where the plate is clearly visible.
3. Enter that time in **“Video second to inspect.”**
4. Click **“Show detected regions.”**
5. Check the green boxes and the face/plate counts.

Interpretation:

- The plate is visible and there is no green box → the baseline missed it.
- The box covers only part of the plate → the detector found it, but localization is inaccurate.
- The box covers the plate, but the processed result is readable → we need stronger blur or a larger region.

The diagnostic frame stays in the local app. Do not upload your video or frames containing other people’s faces or plates to GitHub.

## Terms

- **Detector** — an algorithm that reports where objects are in a frame.
- **Bounding box** — a rectangle around a detected object.
- **False negative (FN)** — an object is present, but the detector misses it.
- **False positive (FP)** — the detector marks a region that contains no target object.
- **Localization** — how closely the predicted box matches the object boundaries.
- **Post-processing** — operations after detection. In this app, that means expanding the box and blurring its pixels.

## Record the observation

For each inspected frame, record:

| Field | Value |
|---|---|
| Object type | face / plate |
| Video timestamp | seconds |
| Box found | yes / no |
| Box covers the full object | yes / no |
| Object readable after blur | yes / no |
| Likely cause | miss / small box / weak blur |

This is a small manual error analysis. Later, we will annotate frames and calculate recall: the fraction of real objects found by the detector.

## Next step

After inspecting a few frames, we will compare Haar Cascade with a neural detector and decide whether fine-tuning is needed. OpenCV Zoo provides LPD-YuNet, but its authors state that it was trained on Chinese license plates and may perform worse on other formats. We will check it against the relevant plate type before treating it as a solution, or prepare data for fine-tuning. See the [OpenCV Zoo model notes](https://github.com/opencv/opencv_zoo/tree/main/models/license_plate_detection_yunet).

## Related material

- [Step 1: Haar Cascade and blur](STEP_01_BASELINE.md)
- [Glossary](GLOSSARY.md)
- [Project plan](PROJECT_PLAN.md)
