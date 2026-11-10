# Animated Shorts

A Remotion + three.js project for vertical cartoon shorts (2D characters in a 3D world), set up from the
`cartoon-3d-short` skill (`../.claude/skills/cartoon-3d-short/`, mromidev/claude-animated-shorts at commit e3b817b).
The example short "The Bridge That Fell for a Song" is in `src/videos/bridge/`.

## Set up on your computer
1. Install [Git](https://git-scm.com/), [Node.js LTS](https://nodejs.org/), [Python 3](https://www.python.org/) and
   [ffmpeg](https://ffmpeg.org/download.html).
2. Download this repo and install the packages:
   ```bash
   git clone https://github.com/cheapcomplex-svg/asdas.git
   ```
   ```bash
   cd asdas/animated-shorts
   ```
   ```bash
   npm install
   ```
   ```bash
   pip install numpy scipy pillow
   ```
3. So Claude Code can use the skill in any folder, copy `.claude/skills/cartoon-3d-short` into `~/.claude/skills/`.
   (Inside this repo it already works without copying.)

## Everyday commands
- Preview in the browser: `npm run studio`
- Test stills (frames 100 and 400 at half size): `npm run still`
- Final 2K render: `npm run render`

## Settings (environment variables)
| Variable | What it does | Default |
|---|---|---|
| `REMOTION_TMP` | Where render temp files go. Each render copies ~1.3 GB here, so point it at your biggest drive and clean it out between projects. | `./remotion-tmp` |
| `CHROME_PATH` | Chrome to render with | Remotion downloads its own |
| `REMOTION_GL` | `angle` uses your graphics card; `swangle` is slow software rendering for machines without one | `angle` |

Windows example (PowerShell), for a big D: drive: `setx REMOTION_TMP "D:\remotion-tmp"` (open a new terminal afterwards).
Mac/Linux: add `export REMOTION_TMP="/path/to/big/drive/remotion-tmp"` to your shell profile.

## Not included
- **Kenney 3D props** (trees, bushes, lanterns, carts…): free CC0 models from kenney.nl (Nature Kit and similar).
  Put the `.glb` files in `public/bridge/kenney/` with the names listed in `src/videos/bridge/world.ts` (`KENNEY`).
  Without them the video still renders, just without those props.
- **Voice**: put `voice.wav` and `words.json` (word timings) in `voice/` before running the sound scripts in `audio/`.
