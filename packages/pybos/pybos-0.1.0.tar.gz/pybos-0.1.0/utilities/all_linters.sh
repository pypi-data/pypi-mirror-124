#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "${SCRIPT_DIR}/.." || exit 1

echo "** python **"
isort .
black .
pflake8
mypy .
pylint pybos
pydocstyle

echo "** shell scripts **"
shfmt -i 2 -ci -w -d utilities
shellcheck utilities/*.sh
