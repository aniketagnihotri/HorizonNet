FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt requirements-dev.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy source code
COPY src/ src/
COPY examples/ examples/
COPY tests/ tests/

# Set PYTHONPATH
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Default command
CMD ["python", "examples/credit_assessment_demo.py"]
