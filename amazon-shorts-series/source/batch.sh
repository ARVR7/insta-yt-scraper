#!/usr/bin/env bash
cd "$(dirname "$0")"
names=(x the_vanishing who_was_fawcett the_city_of_z the_one_rule dead_horse_camp silence the_search_parties the_bones four_theories was_he_right)
for p in 1 2 3 4 5 6 7 8 9 10; do
  if [ $p = 1 ]; then python3 part1.py full silent_$p.mp4 > log_$p.txt 2>&1; else python3 series_parts.py full $p silent_$p.mp4 > log_$p.txt 2>&1; fi
  f=$(printf "out/part%02d_%s.mp4" $p ${names[$p]})
  ffmpeg -y -loglevel error -i silent_$p.mp4 -i audio_p$p.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$f" && echo "part $p done $f" >> batch.log
done
echo ALLDONE >> batch.log
