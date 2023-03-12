#!/bin/bash

# download videos from youtube

mkdir -p youtube
grep youtube.com/watch "ExistingDocumentation.md" \
	| sed \
		-e 's|.*\](http[s]\?://www.youtube.com/watch|https://www.youtube.com/watch|' \
		-e 's|)$||' \
	| xargs -n 1 youtube-dl -o 'youtube/%(id)s.%(ext)s'
