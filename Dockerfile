# Use a smaller base image if possible
FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install LaTeX packages and other dependencies in one RUN command to minimize layers
# Clean up the apt cache in the same layer to reduce image size
RUN apt-get update && apt-get install -y \
    make \
    pandoc \
    texlive-xetex \
    texlive-fonts-extra \
    wget \
    fonts-roboto-slab \
    ghostscript \
    python3 \
    python3-pip \
    && wget --output-document=/usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 \
    && chmod +x /usr/local/bin/yq \
    && yq --version \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# bind mount requirements.txt and install python dependencies
# Note: This will only work during a Docker build if you use BuildKit, otherwise, you need to copy the requirements.txt file
# and run pip install as a separate step during container runtime.
RUN --mount=type=bind,target=/latex_content pip3 install -r /latex_content/requirements.txt

# Set working directory
WORKDIR /latex_content

# Default command to compile the LaTeX document using XeLaTeX
# This command can be overridden when running the container
CMD ["make", "pdf"]
