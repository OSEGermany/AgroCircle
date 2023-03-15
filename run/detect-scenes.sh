#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2014 Thomas Kalka <thomas.kalka@co-buero.de>
# SPDX-FileCopyrightText: 2020-2023 Robin Vobruba <hoijui.quaero@gmail.com>
# SPDX-License-Identifier: CC-BY-SA-4.0

# Exit immediately on each error and unset variable;
# see: https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail
#set -Eeu

# Extracta scene changes from youtube-video.
# NOTE This requires real ffmpeg, not libav
#      (which is bundled with debian)

INF="$1"

echo "Processing $INF ..."

ID=$(basename "$INF" .mp4)
DIR=$(dirname "$INF")

ffmpeg \
	-v debug \
	-i "$INF" \
	-vf "select='gt(scene\,0.35)'" \
	-vsync 0 \
	-f image2 \
	"$DIR/$ID-%04d.jpg" \
	2>&1 \
	| cat > "$DIR/$ID.frames"
grep select:1 "$DIR/$ID.frames" > "$DIR/$ID.scenes"
cat "$DIR/$ID.scenes"
