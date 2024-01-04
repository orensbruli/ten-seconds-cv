
# Use an official Ubuntu base image
FROM ubuntu:latest

# Install LaTeX packages
RUN apt-get update && apt-get install -y \
    texlive \
    texlive-xetex \
    texlive-lualatex \
    texlive-math-extra \
    texlive-fonts-extra \
    texlive-pstricks

# Set working directory
WORKDIR /usr/src/app

# Copy the LaTeX files into the container
COPY . .

# Note: For Font Awesome support, compile with LuaLaTeX instead of XeLaTeX
# Default command to compile the LaTeX document using XeLaTeX
# This command can be overridden when running the container
CMD ["xelatex", "template.tex"]
