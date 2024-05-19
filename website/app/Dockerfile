FROM public.ecr.aws/lambda/python:3.11

# Install libGL and other dependencies
RUN yum install -y mesa-libGL gcc

# Copy function code and model files
COPY whatispants/app.py ${LAMBDA_TASK_ROOT}
COPY whatispants/requirements.txt ${LAMBDA_TASK_ROOT}
COPY whatispants/lvis_fash_m_50.pt ${LAMBDA_TASK_ROOT}

# Install Python dependencies
RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["app.lambda_handler"]
