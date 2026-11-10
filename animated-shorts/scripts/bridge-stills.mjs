// usage: node scripts/bridge-stills.mjs <outPrefix> <frame,frame,...> [scale]  (bundles once, GPU via ANGLE, jpeg)
// BRIDGE_ENTRY=src/sandboxes/<name>/index.tsx renders a sandbox copy instead of the main project entry.
import fs from "node:fs";
// Remotion bundles fill the temp folder (~1.3 GB each): keep them in REMOTION_TMP (a folder on your biggest drive).
// Defaults to ./remotion-tmp inside this project.
const tmp = (await import("node:path")).resolve(process.env.REMOTION_TMP || "remotion-tmp");
fs.mkdirSync(tmp, { recursive: true });
process.env.TEMP = process.env.TMP = process.env.TMPDIR = tmp;
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
const [prefix, frames, scale = "0.5"] = process.argv.slice(2);
// Uses CHROME_PATH if set; otherwise Remotion downloads and uses its own headless Chrome.
const browserExecutable = process.env.CHROME_PATH || null;
// GL backend: "angle" uses your graphics card; set REMOTION_GL=swangle on machines without one (slow software rendering).
const chromiumOptions = { gl: process.env.REMOTION_GL || "angle" };
const serveUrl = await bundle({ entryPoint: path.resolve(process.env.BRIDGE_ENTRY || "src/index.ts"), publicDir: path.resolve("public") });
const composition = await selectComposition({ serveUrl, id: "BridgeShort", browserExecutable, chromiumOptions });
const onBrowserLog = (l) => { if (l.type === "error" || l.type === "warning") console.log(`[${l.type}]`, l.text.slice(0, 300)); };
for (const f of frames.split(",").map(Number)) {
  const t0 = Date.now();
  await renderStill({ composition, serveUrl, frame: f, output: `${prefix}${f}.jpg`, imageFormat: "jpeg", jpegQuality: 88, scale: Number(scale),
    browserExecutable, chromiumOptions, timeoutInMilliseconds: 180000, onBrowserLog });
  console.log("still", f, ((Date.now() - t0) / 1000).toFixed(1) + "s");
}
