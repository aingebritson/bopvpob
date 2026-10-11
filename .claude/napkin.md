# Napkin Runbook

## Curation Rules
- Re-prioritize on every read.
- Keep recurring, high-value notes only.
- Max 10 items per category.
- Each item includes date + "Do instead".

## Execution & Validation (Highest Priority)
1. **[2026-10-11] Game ships as a claude.ai Artifact, not a local file**
   Do instead: after edits, republish `index.html` with the Artifact tool. From a new session pass `url: https://claude.ai/artifact/GwfKEe87qFZYan4fSU2CUo` (read it first) so the link the user's wife has keeps working.
2. **[2026-10-11] Two deploy targets: Claude artifact AND GitHub Pages**
   Do instead: after a change, commit + `git push` (repo `aingebritson/bopvpob`, branch `main`; Pages serves the root at https://aingebritson.github.io/bopvpob/ within ~1 min) and republish the artifact. Only commit/push when the user asks or has approved shipping the change.
3. **[2026-10-11] It's an installable home-screen app (manifest + icons)**
   Do instead: if the look changes, redraw the icon with `tools/make_icon.py` (Pillow; use a scratchpad venv, it's not installed system-wide). Keep the head `<link rel="manifest">`/apple-touch-icon tags; home-screen name is "Pee vs Bees" in both the manifest and `apple-mobile-web-app-title`.
4. **[2026-10-11] `index.html` has no doctype/html/head/body (the Artifact skeleton wraps it)**
   Do instead: for local playtesting, wrap it (`<!doctype html>…<body>` + file + `</body></html>`) into a scratchpad `test/index.html`, point `.claude/launch.json` "game-test" `--directory` at that folder, then `preview_start` "game-test". Rebuild the wrapper after every edit.
5. **[2026-10-11] Syntax-check before testing**
   Do instead: `sed -n '/<script>/,/<\/script>/p' index.html | sed '1d;$d' > game.js && node --check game.js`.
6. **[2026-10-11] Test phone layouts in the browser pane**
   Do instead: `resize_window` preset mobile (portrait) and 812x375 (landscape); drive input with dispatched `PointerEvent`s on `#c` (left half = duck, right half = jump); reset to desktop after.

## Domain Behavior Guardrails
1. **[2026-10-11] Game rules are per-mode in `MODES` (normal / juni); `runMode` is locked at run start**
   Do instead: tune difficulty, patterns, buffer, minJump via `MODES.*`, never hard-code. Juni mode is jump-only, no Top 10 (`noBoard`), separate best (`bopvpob.best.juni`); keep it that way.
2. **[2026-10-11] Global leaderboard lives in `leaderboard/` (Cloudflare Worker + D1)**
   Do instead: `cd leaderboard && npx wrangler ...` (deploy: `npm run deploy`; list: `npm run scores`). CORS allows only aingebritson.github.io + localhost:8765, so local tests must serve on port 8765. Delete any TEST rows you post (`DELETE FROM scores WHERE name = 'TEST'`). Server rate limit: one post per IP per 10s.
3. **[2026-10-11] Hives must be ducked; queens may be jumped or ducked**
   Do instead: keep the hive hitbox top open-ended (`box[3] = 9999`, the drawn rope is part of the obstacle). Don't give queens the same treatment.
4. **[2026-10-11] Browser pane hidden = requestAnimationFrame paused, game clock frozen**
   Do instead: for logic tests, use a test-only copy that exposes `window.__dbg = { obstacles, player, step, render }` (insert just before `function resetPlayer()`, after `player` exists) and step `update(STEP)` directly from an in-page script; the javascript tool can't see page globals.
5. **[2026-10-11] Canvas: `restore()` after `clip()` does not restore the path**
   Do instead: rebuild the shape's path (`beginPath` + shape) before stroking an outline after any clipped fill.
6. **[2026-10-11] Portrait phones need the closer camera**
   Do instead: keep `VIEW_W_PORTRAIT` (480) vs `VIEW_W` (600); if sprites/speeds change, re-check reaction time = (viewRight - PLAYER_X) / speedAt(t).

## User Directives
1. **[2026-10-11] No multi-layer parallax: it made the user's wife dizzy**
   Do instead: ground + obstacles move at game speed; ALL scenery (clouds, hills, trees) moves together at `BACKDROP_SPEED`. Don't add new layers with their own speeds.
2. **[2026-10-11] Art direction: boxy 90s, "less smooth", but NOT pixel art**
   Do instead: straight-edged polygons and boxes, flat two-tone shading (lit/shaded side), banded sky (no gradients), stepped animation (4-frame run cycle, 12fps jitter via `stepT()`), square UI with bevels and hard shadows. Never pixelate the artwork or use `imageSmoothingEnabled=false` tricks.
3. **[2026-10-11] Text is the exception: old-school arcade lettering IS wanted**
   Do instead: Press Start 2P for headings/buttons/score/canvas text (uppercase, square `--px-outline` text-shadow, canvas `blockText()`), Pixelify Sans for small body text. No smooth `-webkit-text-stroke` outlines; fade-outs blink instead.
4. **[2026-10-11] Duck-under obstacles are crowned queen bees; swarm/hive bees wear army helmets**
   Do instead: keep `queen` kind + `drawQueen()` distinct from `drawBee()`.
5. **[2026-10-11] Copy is minimal and hers: no joke quips on the game-over card, no themed puns in popups**
   Do instead: keep game-over to "Soaked!", time, New best badge, "Try again"; pause card is just "Paused" + "Keep running"; popups stay short (OOF!/TRIP!/WHOA!/BZZT!/OUCH!). Ask before adding new flavor text.
6. **[2026-10-11] Obstacles must contrast with the green backdrop**
   Do instead: no green obstacles (bushes became brown dirt piles); check new obstacle colors against hills/trees.
7. **[2026-10-11] Built for the user's wife, played on a phone**
   Do instead: design touch-first (portrait default), keep keyboard as a bonus.
8. **[2026-10-11] Runner holds the balloon in their arms; v1 is generic**
   Do instead: don't add dream-specific characters/setting until the user supplies details.
