#!/usr/bin/env python3
"""Rasterise SVG figures to PNG and print HTML to PDF with headless Chromium."""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.environ.get("CHROME", "/inner_container/opt/playwright/chromium_headless_shell-1232/"
                        "chrome-headless-shell-linux64/chrome-headless-shell")
FONTS = os.path.join(ROOT, "fonts")

FONT_CSS = f"""
@font-face {{ font-family: 'DejaVu LGC Sans'; src: url('file://{FONTS}/DejaVuLGCSans.woff2'); }}
@font-face {{ font-family: 'DejaVu LGC Sans'; font-weight: bold; src: url('file://{FONTS}/DejaVuLGCSans-Bold.woff2'); }}
@font-face {{ font-family: 'DejaVu LGC Serif'; src: url('file://{FONTS}/DejaVuLGCSerif.woff2'); }}
@font-face {{ font-family: 'DejaVu LGC Serif'; font-style: italic; src: url('file://{FONTS}/DejaVuLGCSerif-Italic.woff2'); }}
@font-face {{ font-family: 'DejaVu LGC Serif'; font-weight: bold; src: url('file://{FONTS}/DejaVuLGCSerif-Bold.woff2'); }}
@font-face {{ font-family: 'DejaVu LGC Serif'; font-weight: bold; font-style: italic; src: url('file://{FONTS}/DejaVuLGCSerif-BoldItalic.woff2'); }}
"""


def chrome(args):
    subprocess.run([CHROME, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=3000"] + args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def svg_to_png(svg_path, png_path, scale=3):
    svg = open(svg_path).read()
    w = int(float(re.search(r"width='([\d.]+)'", svg).group(1)))
    h = int(float(re.search(r"height='([\d.]+)'", svg).group(1)))
    html = svg_path[:-4] + ".render.html"
    with open(html, "w") as f:
        f.write(f"<html><head><meta charset='utf-8'><style>{FONT_CSS} html,body{{margin:0;padding:0;background:white}}</style></head>"
                f"<body>{svg}</body></html>")
    chrome([f"--screenshot={png_path}", f"--window-size={w},{h}", f"--force-device-scale-factor={scale}", f"file://{html}"])
    os.remove(html)


def html_to_pdf(html_path, pdf_path):
    chrome([f"--print-to-pdf={pdf_path}", "--no-pdf-header-footer", f"file://{html_path}"])


if __name__ == "__main__":
    figdir = os.path.join(ROOT, "manuscript", "figures")
    for fn in sorted(os.listdir(figdir)):
        if fn.endswith(".svg"):
            svg_to_png(os.path.join(figdir, fn), os.path.join(figdir, fn[:-4] + ".png"))
            print("png:", fn)
    if len(sys.argv) > 2:
        html_to_pdf(sys.argv[1], sys.argv[2])
