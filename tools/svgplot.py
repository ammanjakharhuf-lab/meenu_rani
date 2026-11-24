"""Minimal, dependency-free SVG plotting helpers (line plots, step plots, heatmaps).

Only the Python standard library is used so figures can be regenerated in
restricted environments. Heatmaps are rasterised to PNG and embedded as
base64 images inside the SVG.
"""
import base64
import math
import struct
import zlib

FONT = "DejaVu LGC Sans, DejaVu Sans, Noto Sans, Arial, sans-serif"

PALETTE = ["#1b4f9c", "#d1495b", "#2e8b57", "#e09f3e", "#6a4c93", "#3d3d3d", "#00a6a6", "#8c564b"]

# viridis anchor colours (perceptually uniform)
_VIRIDIS = [(68, 1, 84), (72, 40, 120), (62, 74, 137), (49, 104, 142), (38, 130, 142),
            (31, 158, 137), (53, 183, 121), (110, 206, 88), (181, 222, 43), (253, 231, 37)]
_MAGMA = [(0, 0, 4), (28, 16, 68), (79, 18, 123), (129, 37, 129), (181, 54, 122),
          (229, 80, 100), (251, 135, 97), (254, 194, 135), (252, 253, 191)]


def cmap(name, x):
    anchors = _VIRIDIS if name == "viridis" else _MAGMA
    x = 0.0 if x != x else min(max(x, 0.0), 1.0)
    pos = x * (len(anchors) - 1)
    i = min(int(pos), len(anchors) - 2)
    f = pos - i
    a, b = anchors[i], anchors[i + 1]
    return tuple(int(round(a[k] + f * (b[k] - a[k]))) for k in range(3))


def png_bytes(rgb_rows):
    """Encode rows of (r,g,b) tuples as a PNG file (bytes)."""
    h = len(rgb_rows)
    w = len(rgb_rows[0])
    raw = bytearray()
    for row in rgb_rows:
        raw.append(0)
        for r, g, b in row:
            raw += bytes((r, g, b))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def fmt_tick(v, log=False):
    if log:
        e = int(round(math.log10(v)))
        return f"10<tspan baseline-shift='super' font-size='70%'>{e}</tspan>"
    if v == 0:
        return "0"
    if abs(v) >= 1e4 or abs(v) < 1e-3:
        e = int(math.floor(math.log10(abs(v))))
        m = v / 10 ** e
        return f"{m:g}×10<tspan baseline-shift='super' font-size='70%'>{e}</tspan>"
    return f"{v:g}"


def nice_ticks(lo, hi, n=5):
    span = hi - lo
    if span <= 0:
        return [lo]
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if span / step <= n + 0.5:
            break
    start = math.ceil(lo / step - 1e-9) * step
    ticks = []
    v = start
    while v <= hi + 1e-9 * step:
        ticks.append(round(v, 10))
        v += step
    return ticks


class Axes:
    def __init__(self, x, y, w, h, xlim, ylim, xlog=False, ylog=False, xlabel="", ylabel="",
                 title="", letter="", xticks=None, yticks=None, fs=11):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.xlim, self.ylim = xlim, ylim
        self.xlog, self.ylog = xlog, ylog
        self.xlabel, self.ylabel, self.title, self.letter = xlabel, ylabel, title, letter
        self.xticks, self.yticks = xticks, yticks
        self.fs = fs
        self.items = []
        self.legend_items = []

    def _tx(self, v):
        a, b = self.xlim
        if self.xlog:
            v, a, b = math.log10(max(v, 1e-300)), math.log10(a), math.log10(b)
        return self.x + (v - a) / (b - a) * self.w

    def _ty(self, v):
        a, b = self.ylim
        if self.ylog:
            v, a, b = math.log10(max(v, 1e-300)), math.log10(a), math.log10(b)
        return self.y + self.h - (v - a) / (b - a) * self.h

    def line(self, xs, ys, color="#000", width=1.6, dash=None, label=None, step=False, marker=None):
        pts = []
        prev = None
        for xv, yv in zip(xs, ys):
            if yv is None or (self.ylog and yv <= 0) or (self.xlog and xv <= 0):
                prev = None
                pts.append(None)
                continue
            yv = min(max(yv, self.ylim[0] if not self.ylog else self.ylim[0] * 0.5), self.ylim[1] * (1.0 if not self.ylog else 2))
            px, py = self._tx(xv), self._ty(yv)
            if step and prev is not None:
                pts.append((px, prev[1]))
            pts.append((px, py))
            prev = (px, py)
        segs, cur = [], []
        for p in pts:
            if p is None:
                if len(cur) > 1:
                    segs.append(cur)
                cur = []
            else:
                cur.append(p)
        if len(cur) > 1:
            segs.append(cur)
        d = "" if dash is None else f" stroke-dasharray='{dash}'"
        for sgm in segs:
            path = "M" + " L".join(f"{px:.2f},{py:.2f}" for px, py in sgm)
            self.items.append(f"<path d='{path}' fill='none' stroke='{color}' stroke-width='{width}'"
                              f" stroke-linejoin='round'{d} clip-path='url(#clip{id(self)})'/>")
        if marker:
            for xv, yv in zip(xs, ys):
                if yv is None or (self.ylog and yv <= 0):
                    continue
                self.items.append(f"<circle cx='{self._tx(xv):.2f}' cy='{self._ty(yv):.2f}' r='3' fill='{color}'/>")
        if label:
            self.legend_items.append((label, color, dash, width))

    def vline(self, xv, color="#777", dash="4,3", label=None, width=1.0):
        px = self._tx(xv)
        self.items.append(f"<line x1='{px:.2f}' x2='{px:.2f}' y1='{self.y}' y2='{self.y + self.h}' stroke='{color}' "
                          f"stroke-width='{width}' stroke-dasharray='{dash}'/>")
        if label:
            self.items.append(f"<text x='{px + 3:.1f}' y='{self.y + 11}' font-size='{self.fs - 2}' fill='{color}'>{esc(label)}</text>")

    def hline(self, yv, color="#777", dash="4,3", label=None):
        py = self._ty(yv)
        self.items.append(f"<line x1='{self.x}' x2='{self.x + self.w}' y1='{py:.2f}' y2='{py:.2f}' stroke='{color}' "
                          f"stroke-width='1' stroke-dasharray='{dash}'/>")
        if label:
            self.items.append(f"<text x='{self.x + self.w - 3}' y='{py - 3:.1f}' text-anchor='end' font-size='{self.fs - 2}' fill='{color}'>{esc(label)}</text>")

    def span(self, x0, x1, color="#f2c14e", opacity=0.18, label=None):
        a, b = self._tx(x0), self._tx(min(x1, self.xlim[1]))
        self.items.insert(0, f"<rect x='{a:.2f}' y='{self.y}' width='{max(b - a, 0):.2f}' height='{self.h}' fill='{color}' opacity='{opacity}'/>")
        if label:
            self.items.append(f"<text x='{a + 3:.1f}' y='{self.y + self.h - 4}' font-size='{self.fs - 2.5}' fill='#7a5c00'>{esc(label)}</text>")

    def text(self, xv, yv, s, size=None, anchor="start", color="#222"):
        self.items.append(f"<text x='{self._tx(xv):.1f}' y='{self._ty(yv):.1f}' font-size='{size or self.fs - 1}' "
                          f"text-anchor='{anchor}' fill='{color}'>{s}</text>")

    def bars_h(self, labels, lo, hi, base, colors=("#1b4f9c", "#d1495b")):
        """Tornado bars: labels top-to-bottom, lo/hi values relative to base."""
        n = len(labels)
        bh = self.h / n * 0.6
        for i, lab in enumerate(labels):
            cy = self.y + (i + 0.5) * self.h / n
            for val, col in ((lo[i], colors[0]), (hi[i], colors[1])):
                if val is None:
                    continue
                a, b = sorted((self._tx(base), self._tx(val)))
                self.items.append(f"<rect x='{a:.2f}' y='{cy - bh / 2:.2f}' width='{b - a:.2f}' height='{bh:.2f}' fill='{col}' opacity='0.85'/>")
            self.items.append(f"<text x='{self.x - 6}' y='{cy + 4:.1f}' text-anchor='end' font-size='{self.fs - 1}'>{lab}</text>")
        px = self._tx(base)
        self.items.append(f"<line x1='{px:.2f}' x2='{px:.2f}' y1='{self.y}' y2='{self.y + self.h}' stroke='#222' stroke-width='1.2'/>")

    def legend(self, x=None, y=None, cols=1, size=None):
        fs = size or self.fs - 1.5
        x = self.x + 8 if x is None else x
        y = self.y + 8 if y is None else y
        out = []
        per = math.ceil(len(self.legend_items) / cols)
        colw = 150
        for i, (lab, col, dash, wdt) in enumerate(self.legend_items):
            cx = x + (i // per) * colw
            cy = y + (i % per) * (fs + 5)
            d = "" if dash is None else f" stroke-dasharray='{dash}'"
            out.append(f"<line x1='{cx}' x2='{cx + 22}' y1='{cy + fs / 2:.1f}' y2='{cy + fs / 2:.1f}' stroke='{col}' stroke-width='{wdt + 0.4}'{d}/>")
            out.append(f"<text x='{cx + 27}' y='{cy + fs - 1:.1f}' font-size='{fs}'>{esc(lab)}</text>")
        self.items.extend(out)

    def render(self, frame=True, ticks=True):
        o = [f"<clipPath id='clip{id(self)}'><rect x='{self.x}' y='{self.y}' width='{self.w}' height='{self.h}'/></clipPath>"]
        if frame:
            o.append(f"<rect x='{self.x}' y='{self.y}' width='{self.w}' height='{self.h}' fill='none' stroke='#222' stroke-width='1'/>")
        if ticks:
            if self.xlog:
                xt = self.xticks or [10 ** e for e in range(math.ceil(math.log10(self.xlim[0]) - 1e-9), math.floor(math.log10(self.xlim[1]) + 1e-9) + 1)]
            else:
                xt = self.xticks or nice_ticks(*self.xlim)
            for v in xt:
                px = self._tx(v)
                o.append(f"<line x1='{px:.2f}' x2='{px:.2f}' y1='{self.y + self.h}' y2='{self.y + self.h + 4}' stroke='#222'/>")
                o.append(f"<text x='{px:.2f}' y='{self.y + self.h + 15 + (2 if self.xlog else 0)}' font-size='{self.fs - 1}' text-anchor='middle'>{fmt_tick(v, self.xlog)}</text>")
            if self.ylog:
                yt = self.yticks or [10 ** e for e in range(math.ceil(math.log10(self.ylim[0]) - 1e-9), math.floor(math.log10(self.ylim[1]) + 1e-9) + 1)]
            else:
                yt = self.yticks or nice_ticks(*self.ylim)
            for v in yt:
                py = self._ty(v)
                o.append(f"<line x1='{self.x - 4}' x2='{self.x}' y1='{py:.2f}' y2='{py:.2f}' stroke='#222'/>")
                o.append(f"<text x='{self.x - 6}' y='{py + 4:.2f}' font-size='{self.fs - 1}' text-anchor='end'>{fmt_tick(v, self.ylog)}</text>")
        if self.xlabel:
            o.append(f"<text x='{self.x + self.w / 2}' y='{self.y + self.h + 34}' font-size='{self.fs}' text-anchor='middle'>{self.xlabel}</text>")
        if self.ylabel:
            cx, cy = self.x - 48, self.y + self.h / 2
            o.append(f"<text x='{cx}' y='{cy}' font-size='{self.fs}' text-anchor='middle' transform='rotate(-90 {cx} {cy})'>{self.ylabel}</text>")
        if self.title:
            o.append(f"<text x='{self.x + self.w / 2}' y='{self.y - 7}' font-size='{self.fs}' text-anchor='middle' font-weight='bold'>{self.title}</text>")
        if self.letter:
            o.append(f"<text x='{self.x - 52}' y='{self.y - 8}' font-size='{self.fs + 4}' font-weight='bold'>{self.letter}</text>")
        o.extend(self.items)
        return "\n".join(o)


def heatmap_image(grid, vmin, vmax, x, y, w, h, cm="viridis", log=False):
    rows = []
    n = len(grid)
    for j in range(n - 1, -1, -1):
        row = []
        for v in grid[j]:
            if log:
                v = math.log10(max(v, vmin))
                f = (v - math.log10(vmin)) / (math.log10(vmax) - math.log10(vmin))
            else:
                f = (v - vmin) / (vmax - vmin)
            row.append(cmap(cm, f))
        rows.append(row)
    data = base64.b64encode(png_bytes(rows)).decode()
    return (f"<image x='{x}' y='{y}' width='{w}' height='{h}' preserveAspectRatio='none' "
            f"style='image-rendering:pixelated' href='data:image/png;base64,{data}'/>"
            f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='none' stroke='#222' stroke-width='0.8'/>")


def colorbar(x, y, w, h, vmin, vmax, label, cm="viridis", ticks=None, log=False, fs=10):
    rows = []
    n = 100
    for j in range(n):
        f = 1 - j / (n - 1)
        rows.append([cmap(cm, f)] * 4)
    data = base64.b64encode(png_bytes(rows)).decode()
    o = [f"<image x='{x}' y='{y}' width='{w}' height='{h}' preserveAspectRatio='none' href='data:image/png;base64,{data}'/>",
         f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='none' stroke='#222' stroke-width='0.8'/>"]
    ticks = ticks or ([vmin, (vmin + vmax) / 2, vmax] if not log else None)
    for v in ticks:
        if log:
            f = (math.log10(v) - math.log10(vmin)) / (math.log10(vmax) - math.log10(vmin))
        else:
            f = (v - vmin) / (vmax - vmin)
        py = y + h - f * h
        o.append(f"<line x1='{x + w}' x2='{x + w + 3}' y1='{py:.1f}' y2='{py:.1f}' stroke='#222'/>")
        o.append(f"<text x='{x + w + 5}' y='{py + 3.5:.1f}' font-size='{fs - 1}'>{fmt_tick(v, log)}</text>")
    cx, cy = x + w + 34, y + h / 2
    o.append(f"<text x='{cx}' y='{cy}' font-size='{fs}' text-anchor='middle' transform='rotate(90 {cx} {cy})'>{label}</text>")
    return "\n".join(o)


def svg_doc(width, height, body):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' width='{width}' height='{height}' "
            f"viewBox='0 0 {width} {height}' font-family='{FONT}' font-size='11'>"
            f"<rect width='{width}' height='{height}' fill='white'/>\n{body}\n</svg>")
