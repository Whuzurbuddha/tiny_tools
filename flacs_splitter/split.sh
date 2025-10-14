#!/bin/bash

MUSIC_DIR="$HOME/Music"

find "$MUSIC_DIR" -type f -name "*.cue" | while read -r CUEFILE; do
    DIR=$(dirname "$CUEFILE")
    cd "$DIR" || continue

    FLACFILE=$(awk 'BEGIN{IGNORECASE=1} /^FILE / {match($0, /FILE "(.*)" WAVE/, m); print m[1]; exit}' "$CUEFILE")

    if [[ ! -f "$FLACFILE" ]]; then
        echo "FLAC not found for $CUEFILE â†’ ($FLACFILE) â€“ skip"
        continue
    fi

    echo "Processing: $(basename "$FLACFILE")"

    RATE=$(soxi -r "$FLACFILE")
    BIT=$(soxi -b "$FLACFILE")
    CD_FLAC="$FLACFILE"

    if [[ "$RATE" != "44100" || "$BIT" != "16" ]]; then
        echo "Converting $FLACFILE to 44.1kHz / 16bit..."
        CD_FLAC="${FLACFILE%.flac}_cd.flac"
        ffmpeg -y -i "$FLACFILE" -ar 44100 -sample_fmt s16 "$CD_FLAC"
    fi

    cuebreakpoints "$CUEFILE" | shnsplit -t "%n - %p - %t" -f "$CUEFILE" -o flac "$CD_FLAC"

    cuetag "$CUEFILE" split-track*.flac

    echo "Renaming split tracks..."

    IFS=$'\n'
    mapfile -t TITLES < <(awk '/^TRACK/{i++} /^  TITLE /{gsub(/"/,""); titles[i]=$2} END {for (j=1;j<=i;j++) print titles[j]}' "$CUEFILE")

	
    n=1
	
    for f in split-track*.flac; do
    	
	TITLE="${TITLES[$((n-1))]}"
    	TRACKNUM=$(printf "%02d" "$n")

    	if [[ -z "$TITLE" ]]; then
        	TITLE="Track $TRACKNUM"
    	fi

    	NEWNAME="${TRACKNUM} - ${TITLE}.flac"
    	NEWNAME=$(echo "$NEWNAME" | tr '/:"*?<>|' '_' | sed 's/ *$//')

    	mv -v "$f" "$NEWNAME"
    	((n++))
	done
done

