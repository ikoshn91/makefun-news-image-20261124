# THE WORLD TODAY — Tuesday 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/ikoshn91/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/ikoshn91/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One-page atlas dashboard summing up Tuesday 24 November 2026 world news:
38 dated stories in 8 regions, for make.fun's news-image-20261124 bounty
($100 in USDC, 50 places paid).

The front page leads with the Dow topping 50,000 for the first time
(closing at 50,018.70 as tech slid), Nvidia chief Jensen Huang apologizing
a day after his return, and Russia firing 96 drones at Ukraine. A market
heatmap strip, eight colour-coded region panels and a ticker carry the rest
of the day: the Iran standoff, COP31's flop, the AI sell-off, and Tuesday's
Champions League night.

`gen_image.py` draws the image with Pillow (DejaVu fonts, no downloaded
images, no network, deterministic — two runs produce byte-identical files).
`main.ts` (Node 22, standard library only) copies `entry.png` into
`MAKEFUN_OUTPUT_DIR` (default `/output`) and refuses if it is over 1 MiB.
