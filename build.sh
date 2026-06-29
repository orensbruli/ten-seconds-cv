#!/bin/sh
set -e

FORMAT=${1:-all}

case "$FORMAT" in
  all|both)
    docker run --rm -v "$(pwd)":/latex_content \
      ghcr.io/orensbruli/latex-build:latest \
      make pdf-all
    ;;
  plain|two-columns)
    docker run --rm -v "$(pwd)":/latex_content \
      ghcr.io/orensbruli/latex-build:latest \
      make pdf FORMAT="$FORMAT"
    ;;
  clean)
    rm -rf build
    ;;
  *)
    echo "Usage: $0 [plain|two-columns|all|clean]"
    exit 1
    ;;
esac
