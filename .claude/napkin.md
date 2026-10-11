# Napkin Runbook

## Curation Rules
- Re-prioritize on every read.
- Keep recurring, high-value notes only.
- Max 10 items per category.
- Each item includes date + "Do instead".

## Execution & Validation (Highest Priority)
1. **[2026-10-11] Game ships as a claude.ai Artifact, not a local file**
   Do instead: after edits, republish `index.html` with the Artifact tool. From a new session pass `url: https://claude.ai/artifact/GwfKEe87qFZYan4fSU2CUo` (read it first) so the link the user's wife has keeps working.
2. **[2026-10-11] `index.html` has no doctype/html/head/body (the Artifact skeleton wraps it)**
   Do instead: for local playtesting, wrap it (`<!doctype html>…<body>` + file + `</body></html>`) into a scratchpad `test/index.html`, point `.claude/launch.json` "game-test" `--directory` at that folder, then `preview_start` "game-test". Rebuild the wrapper after every edit.
3. **[2026-10-11] Syntax-check before testing**
   Do instead: `sed -n '/<script>/,/<\/script>/p' index.html | sed '1d;$d' > game.js && node --check game.js`.
4. **[2026-10-11] Test phone layouts in the browser pane**
   Do instead: `resize_window` preset mobile (portrait) and 812x375 (landscape); drive input with dispatched `PointerEvent`s on `#c` (left half = duck, right half = jump); reset to desktop after.

## Domain Behavior Guardrails
1. **[2026-10-11] Canvas: `restore()` after `clip()` does not restore the path**
   Do instead: rebuild the shape's path (`beginPath` + shape) before stroking an outline after any clipped fill.
2. **[2026-10-11] Portrait phones need the closer camera**
   Do instead: keep `VIEW_W_PORTRAIT` (480) vs `VIEW_W` (600); if sprites/speeds change, re-check reaction time = (viewRight - PLAYER_X) / speedAt(t).

## User Directives
1. **[2026-10-11] Art direction: boxy 90s, "less smooth", but NOT pixel art**
   Do instead: straight-edged polygons and boxes, flat two-tone shading (lit/shaded side), banded sky (no gradients), stepped animation (4-frame run cycle, 12fps jitter via `stepT()`), square UI with bevels and hard shadows. Never pixelate the artwork or use `imageSmoothingEnabled=false` tricks.
2. **[2026-10-11] Text is the exception: old-school arcade lettering IS wanted**
   Do instead: Press Start 2P for headings/buttons/score/canvas text (uppercase, square `--px-outline` text-shadow, canvas `blockText()`), Pixelify Sans for small body text. No smooth `-webkit-text-stroke` outlines; fade-outs blink instead.
3. **[2026-10-11] Duck-under obstacles are crowned queen bees; swarm/hive bees wear army helmets**
   Do instead: keep `queen` kind + `drawQueen()` distinct from `drawBee()`.
4. **[2026-10-11] Copy is minimal and hers: no joke quips on the game-over card, no themed puns in popups**
   Do instead: keep game-over to "Soaked!", time, New best badge, "Try again"; popups stay short (OOF!/TRIP!/WHOA!/BZZT!/OUCH!). Ask before adding new flavor text.
5. **[2026-10-11] Obstacles must contrast with the green backdrop**
   Do instead: no green obstacles (bushes became brown dirt piles); check new obstacle colors against hills/trees.
6. **[2026-10-11] Built for the user's wife, played on a phone**
   Do instead: design touch-first (portrait default), keep keyboard as a bonus.
7. **[2026-10-11] Runner holds the balloon in their arms; v1 is generic**
   Do instead: don't add dream-specific characters/setting until the user supplies details.
