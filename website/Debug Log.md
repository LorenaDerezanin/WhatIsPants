# Debug Log
## 2024-09-01: Trying to use Lambda Python runtime instead of Docker
- Attempted to change function runtime from package type image (Docker) to
  lambda handler with Python runtime:
  `libGL.so.1: cannot open shared object file: No such file or directory`
- The solution was to explicitly list `opencv-python-headless` in the
  `requirements.txt` file, with the exact same version as the
  `opencv-python` that `ultralytics` depends on. That presumably replaces
  the `opencv-python` package with the headless version that does not
  require `libGL`, thus not requiring a docker build.
- However, I can't deploy this as a Lambda function because the size of the
  dependencies is too large. Lambda runtime limits are 250MB, but the total
  package size (without the model) is over 900 MB. Only torch is 321 MB.
  - Yes, I've already extracted the model into a separate file, but the
    dependencies are still too large.
