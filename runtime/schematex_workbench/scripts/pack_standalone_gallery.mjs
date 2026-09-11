import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { execSync } from "child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const htmlSrc = path.join(ROOT, "gold", "level1", "review_gallery.html");

execSync("node scripts/build_review_gallery.mjs", { cwd: ROOT, stdio: "inherit" });

const t = fs.readFileSync(htmlSrc, "utf8");
const dataImage = (t.match(/data:image/g) || []).length;
const relativeSrc = (t.match(/src="\.\.\//g) || []).length;
console.log({ bytes: t.length, dataImage, relativeSrc });
if (dataImage < 10 || relativeSrc > 0) {
  console.error("embed failed");
  process.exit(1);
}

const desk = path.join(process.env.USERPROFILE || "", "Desktop");
const stamp = new Date().toISOString().slice(0, 16).replace(/[-:T]/g, "").slice(0, 12);
const packDir = path.join(process.env.TEMP, `l1_share_${stamp}`);
fs.mkdirSync(packDir, { recursive: true });
fs.copyFileSync(htmlSrc, path.join(packDir, "open_Level1_review.html"));
fs.writeFileSync(
  path.join(packDir, "README.txt"),
  "Unzip, then double-click open_Level1_review.html\nNo install needed.\n",
  "utf8"
);

const outZip = path.join(desk, `Level1_review_standalone_${stamp}.zip`);
if (fs.existsSync(outZip)) fs.unlinkSync(outZip);

// PowerShell Compress-Archive
const ps = `Compress-Archive -Path '${packDir}\\*' -DestinationPath '${outZip}' -CompressionLevel Optimal`;
execSync(`powershell -NoProfile -Command "${ps}"`, { stdio: "inherit" });
console.log("ZIP", outZip, (fs.statSync(outZip).size / 1024 / 1024).toFixed(2), "MB");
