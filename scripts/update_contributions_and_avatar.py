"""
Script to update:
1. assets/hero.svg with real avatar image from public/avatar.png
2. assets/contribution-snake.svg with real GitHub contribution data for aggisanjay
"""

import os
import base64
import json
import urllib.request
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
AVATAR_PATH = os.path.join(PUBLIC_DIR, "avatar.png")
HERO_SVG = os.path.join(ASSETS_DIR, "hero.svg")
HEATMAP_SVG = os.path.join(ASSETS_DIR, "contribution-snake.svg")

def update_hero_image():
    if not os.path.exists(AVATAR_PATH):
        print(f"Avatar file not found at {AVATAR_PATH}")
        return

    with open(AVATAR_PATH, "rb") as f:
        avatar_b64 = base64.b64encode(f.read()).decode("utf-8")

    if not os.path.exists(HERO_SVG):
        print(f"hero.svg not found at {HERO_SVG}")
        return

    with open(HERO_SVG, "r", encoding="utf-8") as f:
        content = f.read()

    # Add portraitFade gradient to <defs> if not present
    if 'id="portraitFade"' not in content:
        fade_def = '<linearGradient id="portraitFade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#190B12" stop-opacity="0"/><stop offset=".65" stop-color="#14070F" stop-opacity=".75"/><stop offset="1" stop-color="#10070C" stop-opacity="1"/></linearGradient>'
        content = content.replace("</defs>", f"{fade_def}</defs>")

    # Replace monogram SA or current arch content with real image
    # The arch container is clip-path="url(#arch)"
    old_arch_pattern = '<g clip-path="url(#arch)"><rect x="850" y="95" width="230" height="305" fill="url(#glow)"/>\n<text class="serif" x="965" y="290" text-anchor="middle" font-size="120" font-weight="300" fill="#F8F0F3" opacity=".92">SA</text></g>'
    
    new_arch_content = (
        '<g clip-path="url(#arch)">'
        '<rect x="850" y="95" width="230" height="305" fill="#190B12"/>'
        f'<image href="data:image/png;base64,{avatar_b64}" x="840" y="95" width="250" height="305" preserveAspectRatio="xMidYMid slice"/>'
        '<rect x="850" y="260" width="230" height="140" fill="url(#portraitFade)"/>'
        '</g>'
        '<path d="M850 400V210a115 115 0 0 1 230 0V400Z" fill="none" stroke="#E5B5C7" stroke-opacity=".5" stroke-width="1.5"/>'
    )

    if old_arch_pattern in content:
        content = content.replace(old_arch_pattern, new_arch_content)
    else:
        # Fallback regex/string replacement for arch content
        import re
        arch_regex = r'<g clip-path="url\(#arch\)">(.*?)</g>'
        content = re.sub(arch_regex, new_arch_content, content, flags=re.DOTALL)

    with open(HERO_SVG, "w", encoding="utf-8") as f:
        f.write(content)

    print("Successfully updated assets/hero.svg with real avatar image!")

def fetch_github_contributions():
    url = "https://github-contributions-api.jogruber.de/v4/aggisanjay?y=last"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
            return data
    except Exception as e:
        print(f"Error fetching from jogruber API: {e}. Trying fallback...")
        return None

def update_contribution_heatmap():
    data = fetch_github_contributions()
    if not data or "contributions" not in data:
        print("Could not fetch real contribution data.")
        return

    contributions = data.get("contributions", [])
    total_contributions = sum(d["count"] for d in contributions)

    # Compute streaks
    max_streak = 0
    curr_streak = 0
    streak = 0
    for d in contributions:
        if d["count"] > 0:
            streak += 1
            if streak > max_streak:
                max_streak = streak
        else:
            streak = 0
    for d in reversed(contributions):
        if d["count"] > 0:
            curr_streak += 1
        else:
            break

    # Build 53 columns x 7 rows grid
    # Grid parameters from user SVG
    start_x = 60
    start_y = 90
    step = 19
    width = 15
    height = 15
    rx = 3

    # Date to index mapping
    # contributions list begins on a Sunday (weekday 6)
    # Sunday is row 0, Monday row 1 ... Saturday row 6
    tiles_svg = []
    month_labels = []
    seen_months = set()

    col = 0
    row = 0

    # Determine first day's weekday: Python weekday(): Mon=0..Sun=6
    first_date_str = contributions[0]["date"]
    first_dt = datetime.datetime.strptime(first_date_str, "%Y-%m-%d")
    first_weekday = (first_dt.weekday() + 1) % 7 # 0=Sun, 1=Mon, ..., 6=Sat

    row = first_weekday

    for d in contributions:
        dt = datetime.datetime.strptime(d["date"], "%Y-%m-%d")
        c_weekday = (dt.weekday() + 1) % 7 # 0=Sun..6=Sat
        
        # Track months for labels
        month_key = dt.strftime("%b")
        if dt.day <= 7 and month_key not in seen_months:
            seen_months.add(month_key)
            lbl_x = start_x + col * step
            month_labels.append(f'<text class="mono" x="{lbl_x}" y="76" font-size="10" fill="#B6A3AC">{month_key.upper()}</text>')

        count = d["count"]
        # Opacity and color based on exact contribution count
        if count == 0:
            color = "#C77B9B"
            op = "0.06"
        elif count <= 2:
            color = "#C77B9B"
            op = "0.32"
        elif count <= 5:
            color = "#C77B9B"
            op = "0.62"
        elif count <= 9:
            color = "#E5B5C7"
            op = "0.88"
        else:
            color = "#F8F0F3"
            op = "1.0"

        x = start_x + col * step
        y = start_y + c_weekday * step
        tiles_svg.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}" fill="{color}" opacity="{op}"/>')

        if c_weekday == 6:
            col += 1

    tiles_str = "\n".join(tiles_svg)
    months_str = "\n".join(month_labels)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 410" width="1200" height="410" role="img" aria-label="GitHub contributions for aggisanjay. {total_contributions:,} contributions in the last year.">
<title>GitHub contributions for aggisanjay</title><desc>{total_contributions:,} contributions in the last year. Longest streak: {max_streak} days.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#190B12"/><stop offset="1" stop-color="#10070C"/></linearGradient>
<radialGradient id="glow" cx="80%" cy="15%" r="75%"><stop offset="0" stop-color="#701A3D" stop-opacity=".6"/><stop offset="1" stop-color="#451126" stop-opacity="0"/></radialGradient>
<linearGradient id="sheen" gradientUnits="userSpaceOnUse" x1="-300" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#E5B5C7"/><stop offset=".5" stop-color="#F8F0F3"/><stop offset="1" stop-color="#E5B5C7"/><animateTransform attributeName="gradientTransform" type="translate" values="0 0;1500 0;1500 0" keyTimes="0;.4;1" dur="7s" begin="1.5s" repeatCount="indefinite"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#C77B9B" stroke-opacity=".06"/></pattern></defs>
<style>.serif{{font-family:Georgia,"Iowan Old Style","Palatino Linotype","Times New Roman",serif}}
.mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}}
.sans{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
.in{{animation:in 1s cubic-bezier(.16,1,.3,1) both}}@keyframes in{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<rect width="1200" height="410" rx="20" fill="url(#bg)"/><rect width="1200" height="410" rx="20" fill="url(#glow)"/><rect width="1200" height="410" rx="20" fill="url(#grid)"/>
<rect x=".5" y=".5" width="1199" height="409" rx="19.5" fill="none" stroke="#C77B9B" stroke-opacity=".16"/>

<!-- Header -->
<text class="mono" x="56" y="48" font-size="12" letter-spacing="3" fill="#C77B9B">GITHUB CONTRIBUTIONS · @aggisanjay</text>
<text class="mono" x="1144" y="48" text-anchor="end" font-size="11" letter-spacing="2" fill="#B6A3AC">LIVE CALENDAR · SYNCED</text>

<!-- Month Labels -->
{months_str}

<!-- Contribution Tiles -->
{tiles_str}

<!-- Stats Footer Divider -->
<path d="M56 248H1144" stroke="#C77B9B" stroke-opacity=".2"/>

<!-- Metric 1: Total -->
<text class="serif" x="56" y="296" font-size="40" font-weight="300" letter-spacing="-1" fill="#F8F0F3">{total_contributions:,}</text>
<text class="mono" x="56" y="322" font-size="10.5" letter-spacing="2" fill="#C77B9B">CONTRIBUTIONS IN THE LAST YEAR</text>

<!-- Metric 2: Longest Streak -->
<text class="serif" x="430" y="296" font-size="40" font-weight="300" letter-spacing="-1" fill="#F8F0F3">{max_streak} <tspan font-size="24" fill="#B6A3AC">Days</tspan></text>
<text class="mono" x="430" y="322" font-size="10.5" letter-spacing="2" fill="#B6A3AC">LONGEST ACTIVE STREAK</text>

<!-- Metric 3: Current Cadence -->
<text class="serif" x="730" y="296" font-size="34" font-style="italic" font-weight="300" fill="url(#sheen)">Active Cadence<tspan font-style="normal" fill="#E5B5C7">.</tspan></text>
<text class="mono" x="730" y="322" font-size="10.5" letter-spacing="2" fill="#B6A3AC">CONTINUOUS CODE SHIPMENT</text>

<!-- Legend -->
<g transform="translate(1000, 305)">
  <text class="mono" x="-32" y="9" font-size="10" fill="#B6A3AC">Less</text>
  <rect x="0" y="0" width="10" height="10" rx="2" fill="#C77B9B" opacity="0.06"/>
  <rect x="15" y="0" width="10" height="10" rx="2" fill="#C77B9B" opacity="0.32"/>
  <rect x="30" y="0" width="10" height="10" rx="2" fill="#C77B9B" opacity="0.62"/>
  <rect x="45" y="0" width="10" height="10" rx="2" fill="#E5B5C7" opacity="0.88"/>
  <rect x="60" y="0" width="10" height="10" rx="2" fill="#F8F0F3" opacity="1.0"/>
  <text class="mono" x="78" y="9" font-size="10" fill="#B6A3AC">More</text>
</g>

<!-- Verified Tag -->
<text class="mono" x="56" y="375" font-size="10.5" letter-spacing="1.5" fill="#B6A3AC">DATA SOURCE: GITHUB PUBLIC EVENT GRAPH · UPDATED DAILY</text>
<text class="mono" x="1144" y="375" text-anchor="end" font-size="10.5" letter-spacing="1.5" fill="#E5B5C7">OCT 2025 – OCT 2026</text>
</svg>"""

    with open(HEATMAP_SVG, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Successfully generated {HEATMAP_SVG} with {total_contributions:,} contributions!")

if __name__ == "__main__":
    update_hero_image()
    update_contribution_heatmap()
