
# Use an official Ubuntu base image
FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install LaTeX packages
RUN apt-get update && apt-get install -y \
    make \
    pandoc \
    texlive \
    texlive-bibtex-extra \
    texlive-fonts-extra \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-luatex \
    texlive-pstricks \
    texlive-xetex \
    wget

RUN wget --output-document=/usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 && \
    chmod +x /usr/local/bin/yq && \
    yq --version

RUN apt-get update && apt-get install -y \
    fonts-roboto-slab

RUN apt-get update && apt-get install -y \
    ghostscript \
    python3 \
    python3-pip

# bind mount requirements.txt and install python dependencies
RUN --mount=type=bind,target=/latex_content pip3 install -r /latex_content/requirements.txt

# Set working directory
WORKDIR /latex_content

# Note: For Font Awesome support, compile with LuaLaTeX instead of XeLaTeX
# Default command to compile the LaTeX document using XeLaTeX
# This command can be overridden when running the container
CMD ["make", "pdf"]
