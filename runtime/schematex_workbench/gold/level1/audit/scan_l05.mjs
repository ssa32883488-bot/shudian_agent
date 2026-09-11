import fs from "fs";
const svg = fs.readFileSync("gold/level1/cards/L05/gen_tbx.svg", "utf8");
const paths = [...svg.matchAll(/\bd="([^"]+)"/g)].map((m) => m[1]);
const boxes = [
  { n: "Y1", x0: 280, x1: 342, y0: 560, y1: 616 },
  { n: "Y2", x0: 560, x1: 622, y0: 560, y1: 616 },
  { n: "Y3", x0: 980, x1: 1038, y0: 562, y1: 606 },
];
function pts(d) {
  return [...d.matchAll(/[ML]([\d.]+),([\d.]+)/g)].map((m) => [+m[1], +m[2]]);
}
for (const d of paths) {
  const p = pts(d);
  if (p.length < 2) continue;
  for (const b of boxes) {
    for (let i = 0; i < p.length - 1; i++) {
      const [x1, y1] = p[i];
      const [x2, y2] = p[i + 1];
      const xmin = Math.min(x1, x2),
        xmax = Math.max(x1, x2),
        ymin = Math.min(y1, y2),
        ymax = Math.max(y1, y2);
      const crossH = y1 === y2 && y1 > b.y0 + 2 && y1 < b.y1 - 2 && xmin < b.x1 - 5 && xmax > b.x0 + 5;
      const crossV = x1 === x2 && x1 > b.x0 + 2 && x1 < b.x1 - 2 && ymin < b.y1 - 2 && ymax > b.y0 + 2;
      if (crossH || crossV) console.log("THROUGH", b.n, "seg", x1, y1, "->", x2, y2);
    }
  }
}
console.log("scan done");
