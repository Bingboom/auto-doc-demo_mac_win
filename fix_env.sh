#!/bin/zsh
export VIRTUAL_ENV="$(pwd)/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
.venv/bin/python3 "$@"
