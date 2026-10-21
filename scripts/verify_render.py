#!/usr/bin/env python3
"""
scripts/verify_render.py
Renders all SVG assets with Playwright Chromium, waits ~8s to capture
travelling border lights, typing reveal, and flow dots, saves screenshots,
and programmatically verifies that grid cards do not collapse to (0,0).
"""

import os
import glob
from playwright.sync_api import sync_playwright

WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(WORKSPACE, "assets")
OUTPUT_DIR = os.path.join(WORKSPACE, "verification_screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEIGHTS = {
    "hero.svg": 500,
    "about-intro.svg": 440,
    "experience.svg": 390,
    "tech-constellation.svg": 520,
    "impact.svg": 440,
    "github-glance.svg": 400,
    "contribution-snake.svg": 430,
    "footer-signature.svg": 220,
}

def verify_all():
    svg_files = sorted(glob.glob(os.path.join(ASSETS_DIR, "*.svg")))
    print(f"Verifying {len(svg_files)} SVGs in assets/...")

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for svg_path in svg_files:
            filename = os.path.basename(svg_path)
            png_name = filename.replace(".svg", ".png")
            png_path = os.path.join(OUTPUT_DIR, png_name)
            svg_abs = svg_path.replace("\\", "/")

            if filename.startswith("title-"):
                h = 140
            elif filename.startswith("project-"):
                h = 390
            else:
                h = HEIGHTS.get(filename, 400)

            context = browser.new_context(viewport={"width": 1220, "height": h})
            page = context.new_page()

            page.goto(f"file:///{svg_abs}")
            page.wait_for_timeout(5000)
            page.screenshot(path=png_path)
            sz = os.path.getsize(png_path)
            print(f"[OK] {filename} -> {png_name} ({sz:,} bytes)")

            # Check translation bounding boxes
            if filename in ["impact.svg", "tech-constellation.svg", "about-intro.svg"]:
                tile_groups = page.locator("svg > g[transform^='translate']")
                count = tile_groups.count()
                collapsed = False
                for idx in range(count):
                    box = tile_groups.nth(idx).bounding_box()
                    if box and box["x"] < 5 and box["y"] < 5:
                        collapsed = True
                        print(f"  [ERROR] Tile {idx} collapsed to (0,0) in {filename}!")
                if not collapsed:
                    print(f"  [PASS] {filename}: all {count} grid cards confirmed in proper positions, none at (0,0)!")
                results.append((filename, not collapsed))

            context.close()

        browser.close()

    print("\n" + "="*50)
    print("PLAYWRIGHT VERIFICATION SUMMARY")
    for fn, passed in results:
        status = "PASSED" if passed else "FAILED"
        print(f"  {fn}: {status}")
    print("="*50)

if __name__ == "__main__":
    verify_all()
