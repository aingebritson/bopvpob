# Balloon of Pee vs. Platoon of Bees

You're holding a balloon full of pee. Don't let the bees pop it.

A phone-friendly endless runner based on a dream. A platoon of helmeted bees is chasing you. Jump the rocks, dirt piles and fire hydrants, and duck under the queen bees and hanging hives. Every stumble lets the swarm catch up, and the longer you survive, the faster it gets. Sooner or later they always catch you. The goal is to stay dry as long as you can.

**Play it:** https://aingebritson.github.io/bopvpob/

## Controls

| Phone | Keyboard | Action |
|---|---|---|
| Tap the right half | ↑ or Space | Jump (hold for a higher jump) |
| Hold the left half | ↓ | Duck (tap while in the air to drop fast) |

## Put it on your phone

It installs like an app, with its own icon, and opens full screen.

**iPhone (Safari)**
1. Open https://aingebritson.github.io/bopvpob/ in Safari.
2. Tap the **Share** button (the square with an arrow pointing up). On newer iPhones you may need to tap **•••** first.
3. Scroll down and tap **Add to Home Screen**.
4. If you see **Open as Web App**, leave it on. Tap **Add**.

**Android (Chrome)**
1. Open https://aingebritson.github.io/bopvpob/ in Chrome.
2. Tap the **⋮** menu in the top-right corner.
3. Tap **Add to Home screen** (it may say **Install app**), then **Install**.

A **Pee vs Bees** icon appears on your home screen. No sound on an iPhone? Turn off silent mode.

## How it's built

The whole game is a single file, [`index.html`](index.html): plain JavaScript drawing on an HTML canvas. All the game art is drawn in code and all the sound is synthesized in the browser, so there's nothing to install or build. The PNG files are only the home-screen icon, and `manifest.webmanifest` tells phones how to install it. Open `index.html` in a browser to play locally.
