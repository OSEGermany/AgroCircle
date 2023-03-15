#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2014 Thomas Kalka <thomas.kalka@co-buero.de>
# SPDX-FileCopyrightText: 2020-2023 Robin Vobruba <hoijui.quaero@gmail.com>
# SPDX-License-Identifier: CC-BY-SA-4.0

# Exit immediately on each error and unset variable;
# see: https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail
#set -Eeu

# Downloads youtube videos mentioned in the documentation.

ytdl="$(which yt-dlp || which youtube-dl || echo '')"

if [ -z "$ytdl" ]
then
	>&2 echo "ERROR: Either of the tools yt-dlp (preffered) or youtube-dl are required!"
	exit 1
fi

mkdir -p youtube
grep "youtube.com/watch" "ExistingDocumentation.md" \
	| sed \
		-e 's|.*\](http[s]\?://www.youtube.com/watch|https://www.youtube.com/watch|' \
		-e 's|)$||' \
	| xargs -n 1 "$ytdl" -o 'youtube/%(id)s.%(ext)s'
