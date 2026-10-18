# The Man Who Walked Into the Amazon: 10-part Shorts series

Ten code-rendered YouTube Shorts (17s each, 1080x1920, 30fps, original synthesized audio) telling the Percy Fawcett story. Each part ends on a cliffhanger and carries a "PART N/10" badge.

| Part | File | Cliffhanger |
|---|---|---|
| 1 | videos/part01_the_vanishing.mp4 | The letters stopped. Then 100+ people vanished. |
| 2 | videos/part02_who_was_fawcett.mp4 | Then he found Manuscript 512. |
| 3 | videos/part03_the_city_of_z.mp4 | He told no one where it was. |
| 4 | videos/part04_the_one_rule.mp4 | One last letter left the jungle. |
| 5 | videos/part05_dead_horse_camp.mp4 | After that: silence. |
| 6 | videos/part06_silence.mp4 | A search party came back with something. |
| 7 | videos/part07_the_search_parties.mp4 | They opened the box. Bones. |
| 8 | videos/part08_the_bones.mp4 | It wasn't him. So where was Fawcett? |
| 9 | videos/part09_four_theories.mp4 | Scientists looked from above... |
| 10 | videos/part10_was_he_right.mp4 | He wasn't crazy. He was early. |

## Verify before posting
These facts are from memory and are not confirmed against primary sources: the 100+ searchers figure, Manuscript 512, the 29 May 1925 letter date (also drives the days-missing counter), "no radio", the "not him" bone result, and the Bolivia 2022 / Ecuador 2024 lidar finds.

## Rebuild
Needs Python 3, Pillow, numpy, scipy, ffmpeg and the Inter and DejaVu fonts.

    cd source
    for p in 1 2 3 4 5 6 7 8 9 10; do python3 audio_series.py $p; done   # writes audio_pN.wav
    ./batch.sh                                                             # renders every part into out/

Docs: `docs/series_fawcett_10_shorts.md` (outline and series rules), `docs/script_fawcett_5min.md` (the earlier 5-minute draft).
