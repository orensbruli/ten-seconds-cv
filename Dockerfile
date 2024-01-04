
# Use an official Ubuntu base image
FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install LaTeX packages
RUN apt-get update && apt-get install -y \
    texlive \
    texlive-xetex \
    texlive-luatex \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-pstricks

# Set working directory
WORKDIR /latex_content

# Copy the LaTeX files into the container
COPY . /latex_content

# Note: For Font Awesome support, compile with LuaLaTeX instead of XeLaTeX
# Default command to compile the LaTeX document using XeLaTeX
# This command can be overridden when running the container
CMD ["xelatex", "cv-piotr-kowalski.tex"]
