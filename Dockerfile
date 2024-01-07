
# Use an official Ubuntu base image
FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install LaTeX packages
RUN apt-get update && apt-get install -y \
    pandoc \
    make \
    texlive-bibtex-extra \
    texlive \
    texlive-xetex \
    texlive-luatex \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-pstricks

RUN apt-get update && apt-get install -y \
    wget
# Set working directory
WORKDIR /latex_content

# Note: For Font Awesome support, compile with LuaLaTeX instead of XeLaTeX
# Default command to compile the LaTeX document using XeLaTeX
# This command can be overridden when running the container
CMD ["make", "pdf"]
