# Data and model sources

## Current baseline

The current baseline loads the pretrained Haar cascade XML files packaged with OpenCV:

- frontal-face cascade: `haarcascade_frontalface_default.xml`;
- Russian-style plate cascade: `haarcascade_russian_plate_number.xml`.

The OpenCV package supplies these model files; the project does not redistribute copies. See the [official OpenCV cascade tutorial](https://docs.opencv.org/5.0/tutorials_contrib/xobjdetect/cascade_classifier/cascade_classifier.html) for how pretrained cascades are loaded and applied. The plate classifier is region-specific and is not a universal license-plate model.

## Training data status

No training dataset has been selected or downloaded yet. Before training, we will verify the dataset's image and annotation licenses separately, write down source URLs and versions, and keep source videos and large image archives out of Git. A dataset license does not automatically grant rights to redistribute every model weight trained from it; those terms will be checked too.

## Dataset selection checklist

- Has bounding-box annotations for the complete plate region.
- Includes varied plate sizes, orientations, lighting, and camera distances.
- Has an explicit license for images and annotations.
- Can be split by original source or video so adjacent frames do not leak across train and test.
- Does not require committing private or identifying user videos to the repository.
