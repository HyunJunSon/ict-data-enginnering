#!/bin/bash
dir="${1:-logs}"
for f in "$dir"/*.log; do
 lines=$(wc -l < "$f" | tr -d " " )
 errors=$(grep -c ERROR "$f")
 echo "$f : 전체 ${line}줄 ERROR ${errors}건"
done
