#!/usr/bin/env bash
# Installs the rea-video CLI (github.com/JuneYaooo/rea-video, Apache-2.0) into an isolated venv.
# Run once per fresh session: bash video-studio/tools/install_rea_video.sh
# Then use: ~/rea-video/.venv/bin/rea-video decompose <video.mp4>
set -euo pipefail
DIR="$HOME/rea-video"
[ -d "$DIR/.git" ] || GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 https://github.com/JuneYaooo/rea-video "$DIR"
[ -x "$DIR/.venv/bin/rea-video" ] || { python3 -m venv "$DIR/.venv" && "$DIR/.venv/bin/pip" install -q -e "$DIR[ocr]"; }
"$DIR/.venv/bin/rea-video" --help >/dev/null && echo "rea-video ready: $DIR/.venv/bin/rea-video"
