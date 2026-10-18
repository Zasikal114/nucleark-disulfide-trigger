FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gawk procps curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir gradio pandas pdb-tools huggingface_hub

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null; true

COPY . /app

# Download foldx binary from HF LFS storage
RUN curl -fsSL -o /app/foldx \
    "https://huggingface.co/spaces/kalendar114/Foldx-EV/resolve/main/foldx" && \
    chmod +x /app/foldx && \
    echo "FoldX binary size: $(stat -c%s /app/foldx) bytes" && \
    [ "$(stat -c%s /app/foldx)" -gt 1000000 ] || (echo "ERROR: foldx too small, LFS may not have resolved" && exit 1)

RUN mkdir -p /app/CIF /app/Input /app/results

CMD ["python", "app.py"]
