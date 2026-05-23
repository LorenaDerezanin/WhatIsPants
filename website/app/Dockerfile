FROM public.ecr.aws/lambda/python:3.12

# Copy function code and model files
COPY whatispants/app.py ${LAMBDA_TASK_ROOT}
COPY whatispants/inference.py ${LAMBDA_TASK_ROOT}
COPY whatispants/requirements.txt ${LAMBDA_TASK_ROOT}
COPY whatispants/lvis_fash_m_50.pt ${LAMBDA_TASK_ROOT}

# Install Python dependencies. Install CPU-only torch from PyTorch's CPU
# index first — the PyPI torch wheel for arm64 pulls in the full cuda-toolkit
# + nvidia-* chain (~8 GB) even though Lambda has no GPU.
#
# torch is pinned to 2.6.0 because newer torch (observed on 2.12) raises
# RuntimeError: Failed to initialize cpuinfo! during model.to(device) on
# Lambda — Lambda's /sys/devices/system/cpu/possible is unparseable and torch
# >= 2.7-ish treats that as fatal where 2.6 only warns.
#
# After the install, dedup OpenCV: ultralytics declares opencv-python (the GUI
# variant that needs libGL), and our requirements.txt asks for
# opencv-python-headless — they're separate PyPI distributions so pip installs
# BOTH despite identical versions. Uninstalling opencv-python alone removes
# the shared cv2/ directory (pip's per-distribution RECORD doesn't know two
# packages claim the same files), so we then force-reinstall headless to
# restore cv2. Net result: only headless is present, cv2 still importable,
# no libGL needed at runtime.
RUN pip install --upgrade pip && \
    pip install --index-url https://download.pytorch.org/whl/cpu torch==2.6.0 torchvision==0.21.0 && \
    pip install -r requirements.txt && \
    pip uninstall -y opencv-python && \
    pip install --force-reinstall --no-deps opencv-python-headless==4.11.0.86

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["app.lambda_handler"]
