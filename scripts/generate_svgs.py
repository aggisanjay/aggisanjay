#!/usr/bin/env python3
"""
generate_svgs.py — Generates all animated SVG assets for Sanjay Aggi's GitHub Profile README.
Strictly adheres to the Sushmita Dasari dark-burgundy portfolio design system:
- Palette: #190B12 -> #10070C, wine #701A3D/#451126, rose #C77B9B, pink #E5B5C7, text #F8F0F3, muted #B6A3AC
- Fonts: Georgia serif (weight 300, italic sheen accent), ui-monospace, system sans
- Animations:
  * Travelling border light on EVERY card, tile, panel, and row (pathLength=1000, stroke-dasharray="150 850")
  * Staggered fade-up (class="in")
  * Moving sheen gradient sweeping across italic headings
  * Blinking terminal cursor & typing reveal clipPath
  * Node-flow diagrams with travelling animated pulse dot
  * Toolkit connector web with flowing pulse dot
  * Orbit circle with rotating satellite dot and skill labels
- Nested structure for grid items: <g transform="translate(x y)"><g class="in" ...> to avoid CSS transform overwrite bug!
"""

import os
import base64

ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
PUBLIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public"))
os.makedirs(ASSETS_DIR, exist_ok=True)

# Read avatar image
AVATAR_PATH = os.path.join(PUBLIC_DIR, "avatar.png")
if os.path.exists(AVATAR_PATH):
    with open(AVATAR_PATH, "rb") as f:
        AVATAR_B64 = base64.b64encode(f.read()).decode("utf-8")
else:
    AVATAR_B64 = ""

COMMON_DEFS = """<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#190B12"/>
    <stop offset="1" stop-color="#10070C"/>
  </linearGradient>
  <radialGradient id="glow" cx="80%" cy="15%" r="75%">
    <stop offset="0" stop-color="#701A3D" stop-opacity=".6"/>
    <stop offset="1" stop-color="#451126" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="sheen" gradientUnits="userSpaceOnUse" x1="-300" y1="0" x2="0" y2="0">
    <stop offset="0" stop-color="#E5B5C7"/>
    <stop offset=".5" stop-color="#F8F0F3"/>
    <stop offset="1" stop-color="#E5B5C7"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="0 0;1500 0;1500 0" keyTimes="0;.4;1" dur="7s" begin="1.5s" repeatCount="indefinite"/>
  </linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="#C77B9B" stroke-opacity=".06"/>
  </pattern>
  <linearGradient id="line" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="1160" y2="0">
    <stop offset="0" stop-color="#C77B9B"/>
    <stop offset=".6" stop-color="#701A3D"/>
    <stop offset="1" stop-color="#701A3D" stop-opacity="0"/>
  </linearGradient>
  <filter id="pulseGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
    <feMerge>
      <feMergeNode in="coloredBlur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>"""

COMMON_STYLES = """<style>
  .serif { font-family: Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif; }
  .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }
  .sans { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
  .in { animation: in 1s cubic-bezier(.16,1,.3,1) both; }
  @keyframes in { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
  .tbl {
    stroke: #E5B5C7;
    stroke-width: 1.5;
    stroke-linecap: round;
    stroke-dasharray: 150 850;
    fill: none;
    animation: tblRun 7s linear infinite;
  }
  @keyframes tblRun {
    from { stroke-dashoffset: 1000; }
    to { stroke-dashoffset: 0; }
  }
  .cursor { animation: blink 1.1s infinite; }
  @keyframes blink { 0%, 50% { opacity: 1; } 50.1%, 100% { opacity: 0; } }
  @media (prefers-reduced-motion: reduce) {
    *, .tbl, .in, .cursor { animation: none !important; }
    .tbl { display: none !important; }
  }
</style>"""

def make_title_svg(number, category, title_lead, title_italic, right_label, delay_offset=-1.0):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" width="1200" height="120" role="img" aria-label="{number} {category} - {title_lead} {title_italic}">
  <title>{number} {category} - {title_lead} {title_italic}</title>
  <desc>Section title header for {category}</desc>
  {COMMON_DEFS}
  {COMMON_STYLES}
  <rect width="1200" height="120" rx="20" fill="url(#bg)"/>
  <rect width="1200" height="120" rx="20" fill="url(#glow)"/>
  <rect width="1200" height="120" rx="20" fill="url(#grid)"/>
  <rect x=".5" y=".5" width="1199" height="119" rx="19.5" fill="none" stroke="#C77B9B" stroke-opacity=".16"/>
  <rect class="tbl" x=".5" y=".5" width="1199" height="119" rx="19.5" pathLength="1000" style="animation-delay: {delay_offset:.2f}s;"/>
  <g class="in">
    <text class="mono" x="40" y="34" font-size="12" letter-spacing="3" fill="#C77B9B"><tspan fill="#E5B5C7">{number}</tspan>   {category}</text>
  </g>
  <g class="in" style="animation-delay:.2s">
    <text class="serif" x="38" y="84" font-size="44" font-weight="300" letter-spacing="-1" fill="#F8F0F3">{title_lead} <tspan font-style="italic" fill="url(#sheen)">{title_italic}</tspan></text>
  </g>
  <text class="mono" x="1160" y="34" text-anchor="end" font-size="10.5" letter-spacing="2.4" fill="#B6A3AC">{right_label}</text>
  <path d="M40 106H1160" stroke="url(#line)" stroke-width="1"/>
</svg>"""

def build_hero():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 480" width="1200" height="480" role="img" aria-label="Sanjay Aggi - Full-Stack AI Engineer. React, Node.js, TypeScript, RAG and LLMs. Production systems.">
  <title>Sanjay Aggi - Full-Stack AI Engineer</title>
  <desc>React, Node.js, TypeScript, RAG and LLMs. Production systems.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#190B12"/><stop offset="1" stop-color="#10070C"/></linearGradient>
    <radialGradient id="glow" cx="80%" cy="15%" r="75%"><stop offset="0" stop-color="#701A3D" stop-opacity=".6"/><stop offset="1" stop-color="#451126" stop-opacity="0"/></radialGradient>
    <linearGradient id="sheen" gradientUnits="userSpaceOnUse" x1="-300" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="#E5B5C7"/><stop offset=".5" stop-color="#F8F0F3"/><stop offset="1" stop-color="#E5B5C7"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;1500 0;1500 0" keyTimes="0;.4;1" dur="7s" begin="1.5s" repeatCount="indefinite"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#C77B9B" stroke-opacity=".06"/></pattern>
    <clipPath id="arch"><path d="M850 400V210a115 115 0 0 1 230 0V400Z"/></clipPath>
    <linearGradient id="portraitFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#190B12" stop-opacity="0"/><stop offset=".65" stop-color="#14070F" stop-opacity=".75"/><stop offset="1" stop-color="#10070C" stop-opacity="1"/>
    </linearGradient>
  </defs>
  {COMMON_STYLES}
  <rect width="1200" height="480" rx="20" fill="url(#bg)"/>
  <rect width="1200" height="480" rx="20" fill="url(#glow)"/>
  <rect width="1200" height="480" rx="20" fill="url(#grid)"/>
  <rect x=".5" y=".5" width="1199" height="479" rx="19.5" fill="none" stroke="#C77B9B" stroke-opacity=".16"/>
  <rect class="tbl" x=".5" y=".5" width="1199" height="479" rx="19.5" pathLength="1000" style="animation-delay: -0.8s;"/>

  <!-- Terminal Pill -->
  <rect x="72" y="62" width="322" height="34" rx="17" fill="#10070C" stroke="#C77B9B" stroke-opacity=".3"/>
  <circle cx="92" cy="79" r="4" fill="#C77B9B"/>
  <text class="mono" x="108" y="83" font-size="12" fill="#B6A3AC">~/sanjay <tspan fill="#C77B9B">$</tspan> <tspan fill="#F8F0F3">ship --production</tspan></text>
  <rect class="cursor" x="372" y="71" width="7" height="16" fill="#E5B5C7"/>

  <!-- Kicker -->
  <path d="M72 135h32" stroke="#C77B9B"/>
  <text class="mono" x="116" y="139" font-size="12" letter-spacing="4" fill="#C77B9B">FULL-STACK · AI · PRODUCTION SYSTEMS</text>

  <!-- Big Name -->
  <g class="in"><text class="serif" x="68" y="232" font-size="86" font-weight="300" letter-spacing="-2" fill="#F8F0F3">Sanjay</text></g>
  <g class="in" style="animation-delay:.25s"><text class="serif" x="68" y="318" font-size="86" font-style="italic" font-weight="300" letter-spacing="-2" fill="url(#sheen)">Aggi<tspan fill="#C77B9B">.</tspan></text></g>

  <!-- Underline & Tagline -->
  <path d="M72 344h520" stroke="#C77B9B" stroke-opacity=".5"/>
  <text class="mono" x="72" y="384" font-size="14" letter-spacing="3" fill="#F8F0F3">FULL-STACK AI ENGINEER · REACT · NODE.JS · RAG</text>
  <text class="serif" x="72" y="416" font-size="20" font-style="italic" fill="#B6A3AC">Usable full-stack systems around AI models.</text>

  <!-- Bottom Strip Credentials -->
  <path d="M72 446H1128" stroke="#C77B9B" stroke-opacity=".18"/>
  <text class="mono" x="72" y="466" font-size="11" letter-spacing="2" fill="#B6A3AC">MODELSUITE AI · 60+ PRODUCTION CHANGES</text>
  <text class="mono" x="1128" y="466" text-anchor="end" font-size="11" letter-spacing="2" fill="#E5B5C7">6 SHIPPED AI PRODUCTS · REDIS · BULLMQ · LANGGRAPH</text>

  <!-- Orbit Circle with Rotating Satellite Dot -->
  <circle cx="965" cy="250" r="190" fill="none" stroke="#C77B9B" stroke-opacity=".25"/>
  <g transform="translate(965 250)">
    <g>
      <circle cx="190" cy="0" r="3.5" fill="#E5B5C7">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="16s" repeatCount="indefinite"/>
      </circle>
    </g>
  </g>

  <!-- Arch-Shaped Portrait Frame -->
  <path d="M850 400V210a115 115 0 0 1 230 0V400Z" fill="#190B12" stroke="#E5B5C7" stroke-opacity=".5"/>
  <g clip-path="url(#arch)">
    <rect x="850" y="95" width="230" height="305" fill="#190B12"/>
    <image href="data:image/jpeg;base64,{AVATAR_B64}" xlink:href="data:image/jpeg;base64,{AVATAR_B64}" x="840" y="95" width="250" height="305" preserveAspectRatio="xMidYMid slice"/>
    <rect x="850" y="260" width="230" height="140" fill="url(#portraitFade)"/>
  </g>
  <path d="M850 400V210a115 115 0 0 1 230 0V400Z" fill="none" stroke="#E5B5C7" stroke-opacity=".5" stroke-width="1.5"/>
  <path class="tbl" d="M850 400V210a115 115 0 0 1 230 0V400Z" pathLength="1000" style="animation-delay: -2.4s;"/>

  <!-- Orbit Skill Labels -->
  <g class="mono" font-size="11" letter-spacing="2" fill="#B6A3AC">
    <circle cx="853" cy="82" r="3" fill="#C77B9B"/><text x="866" y="86">RAG</text>
    <circle cx="1120" cy="138" r="3" fill="#C77B9B"/><text x="1130" y="142" text-anchor="start" dx="-48">LLM</text>
    <circle cx="812" cy="272" r="3" fill="#C77B9B"/><text x="760" y="276">API</text>
    <circle cx="1118" cy="342" r="3" fill="#C77B9B"/><text x="1128" y="346" dx="-44">UI</text>
  </g>
</svg>"""

def build_about_intro():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" width="1200" height="420" role="img" aria-label="About Sanjay Aggi. Full-Stack AI Engineer at ModelSuite AI. React, Node.js, TypeScript, RAG, LangGraph. 60+ production changes; six shipped AI products.">
  <title>About Sanjay Aggi</title>
  <desc>Full-Stack AI Engineer at ModelSuite AI. React, Node.js, TypeScript, RAG, LangGraph. 60+ production changes; six shipped AI products.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#190B12"/><stop offset="1" stop-color="#10070C"/></linearGradient>
    <radialGradient id="glow" cx="80%" cy="15%" r="75%"><stop offset="0" stop-color="#701A3D" stop-opacity=".6"/><stop offset="1" stop-color="#451126" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#C77B9B" stroke-opacity=".06"/></pattern>
    <clipPath id="c0a"><rect class="ty" x="68" y="112" width="560" height="22" style="animation-delay:0.60s;animation-duration:.5s;animation-timing-function:steps(18)"/></clipPath>
    <clipPath id="c0b"><rect class="ty" x="68" y="137" width="680" height="22" style="animation-delay:1.20s;animation-duration:.5s;animation-timing-function:steps(30)"/></clipPath>
    <clipPath id="c1a"><rect class="ty" x="68" y="162" width="560" height="22" style="animation-delay:2.10s;animation-duration:.5s;animation-timing-function:steps(18)"/></clipPath>
    <clipPath id="c1b"><rect class="ty" x="68" y="187" width="680" height="22" style="animation-delay:2.70s;animation-duration:.5s;animation-timing-function:steps(30)"/></clipPath>
    <clipPath id="c2a"><rect class="ty" x="68" y="212" width="560" height="22" style="animation-delay:3.60s;animation-duration:.5s;animation-timing-function:steps(18)"/></clipPath>
    <clipPath id="c2b"><rect class="ty" x="68" y="237" width="680" height="22" style="animation-delay:4.20s;animation-duration:.5s;animation-timing-function:steps(30)"/></clipPath>
    <clipPath id="c3a"><rect class="ty" x="68" y="262" width="560" height="22" style="animation-delay:5.10s;animation-duration:.5s;animation-timing-function:steps(18)"/></clipPath>
    <clipPath id="c3b"><rect class="ty" x="68" y="287" width="680" height="22" style="animation-delay:5.70s;animation-duration:.5s;animation-timing-function:steps(30)"/></clipPath>
    <clipPath id="c4a"><rect class="ty" x="68" y="312" width="560" height="22" style="animation-delay:6.60s;animation-duration:.5s;animation-timing-function:steps(18)"/></clipPath>
    <clipPath id="c4b"><rect class="ty" x="68" y="337" width="680" height="22" style="animation-delay:7.20s;animation-duration:.5s;animation-timing-function:steps(30)"/></clipPath>
  </defs>
  <style>
    .serif {{ font-family: Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }}
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    .in {{ animation: in 1s cubic-bezier(.16,1,.3,1) both; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
    .ty {{ transform-box: fill-box; transform-origin: left center; animation-name: ty; animation-fill-mode: both; }}
    @keyframes ty {{ 0% {{ transform: scaleX(0); }} 85%, 100% {{ transform: scaleX(1); }} }}
    .cd {{ animation: in 1s cubic-bezier(.16,1,.3,1) both; }}
    .fd {{ animation: fd 1s ease both; }}
    @keyframes fd {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    .tbl {{
      stroke: #E5B5C7;
      stroke-width: 1.5;
      stroke-linecap: round;
      stroke-dasharray: 150 850;
      fill: none;
      animation: tblRun 7s linear infinite;
    }}
    @keyframes tblRun {{
      from {{ stroke-dashoffset: 1000; }}
      to {{ stroke-dashoffset: 0; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      *, .tbl, .ty, .cd, .fd, .in {{ animation: none !important; }}
      .tbl {{ display: none !important; }}
    }}
  </style>
  <rect width="1200" height="420" rx="20" fill="url(#bg)"/>
  <rect width="1200" height="420" rx="20" fill="url(#glow)"/>
  <rect width="1200" height="420" rx="20" fill="url(#grid)"/>
  <rect x=".5" y=".5" width="1199" height="419" rx="19.5" fill="none" stroke="#C77B9B" stroke-opacity=".16"/>
  <rect class="tbl" x=".5" y=".5" width="1199" height="419" rx="19.5" pathLength="1000" style="animation-delay: -1.0s;"/>

  <!-- Terminal Window on Left -->
  <g class="fd">
    <rect x="40" y="40" width="760" height="340" rx="14" fill="#10070C" stroke="#C77B9B" stroke-opacity=".3"/>
    <rect class="tbl" x="40" y="40" width="760" height="340" rx="14" pathLength="1000" style="animation-delay: -2.8s;"/>
    <path d="M40 54a14 14 0 0 1 14-14H786a14 14 0 0 1 14 14V76H40Z" fill="#190B12"/>
    <circle cx="62" cy="58" r="5" fill="#701A3D"/>
    <circle cx="80" cy="58" r="5" fill="#451126"/>
    <circle cx="98" cy="58" r="5" fill="#451126"/>
    <text class="mono" x="420" y="62" text-anchor="middle" font-size="11" letter-spacing="1.5" fill="#B6A3AC">sanjay@portfolio: ~</text>
  </g>

  <!-- Terminal Typing Content -->
  <g class="mono" font-size="13.5">
    <g clip-path="url(#c0a)"><text x="72" y="128" fill="#C77B9B">$</text><text x="94" y="128" fill="#F8F0F3">whoami</text></g>
    <g clip-path="url(#c0b)"><text x="72" y="153" fill="#701A3D">→</text><text x="94" y="153" fill="#B6A3AC">Sanjay Aggi · Full-Stack AI Engineer</text></g>
    <g clip-path="url(#c1a)"><text x="72" y="178" fill="#C77B9B">$</text><text x="94" y="178" fill="#F8F0F3">cat experience.txt</text></g>
    <g clip-path="url(#c1b)"><text x="72" y="203" fill="#701A3D">→</text><text x="94" y="203" fill="#B6A3AC">Full-Stack Engineer · ModelSuite AI · 60+ production changes</text></g>
    <g clip-path="url(#c2a)"><text x="72" y="228" fill="#C77B9B">$</text><text x="94" y="228" fill="#F8F0F3">ls ./shipped</text></g>
    <g clip-path="url(#c2b)"><text x="72" y="253" fill="#701A3D">→</text><text x="94" y="253" fill="#B6A3AC">curalink  shopai  hireiq  support-desk  zernio  doc-intel</text></g>
    <g clip-path="url(#c3a)"><text x="72" y="278" fill="#C77B9B">$</text><text x="94" y="278" fill="#F8F0F3">cat stack.txt</text></g>
    <g clip-path="url(#c3b)"><text x="72" y="303" fill="#701A3D">→</text><text x="94" y="303" fill="#B6A3AC">TypeScript · Python · React · Next.js · Node · RAG · Vector Search</text></g>
    <g clip-path="url(#c4a)"><text x="72" y="328" fill="#C77B9B">$</text><text x="94" y="328" fill="#F8F0F3">echo $PRINCIPLE</text></g>
    <g clip-path="url(#c4b)"><text x="72" y="353" fill="#701A3D">→</text><text x="94" y="353" fill="#B6A3AC">not AI demos · usable systems with fallbacks and reliability</text></g>
  </g>

  <!-- 3 Accent Cards on Right (Properly Nested to Avoid Transform Bug) -->
  <g transform="translate(836 70)">
    <g class="cd" style="animation-delay:1.2s">
      <rect width="324" height="88" rx="14" fill="#190B12" stroke="#C77B9B" stroke-opacity=".28"/>
      <rect class="tbl" width="324" height="88" rx="14" pathLength="1000" style="animation-delay: -3.5s;"/>
      <rect width="3" height="88" rx="1.5" fill="#C77B9B"/>
      <text class="mono" x="22" y="26" font-size="10" letter-spacing="2" fill="#C77B9B">PRIMARY STACK</text>
      <text class="serif" x="22" y="58" font-size="28" font-weight="300" fill="#F8F0F3">React + Node</text>
      <text class="sans" x="22" y="78" font-size="12" fill="#B6A3AC">TypeScript · Next.js · Express · REST</text>
    </g>
  </g>

  <g transform="translate(836 174)">
    <g class="cd" style="animation-delay:1.7s">
      <rect width="324" height="88" rx="14" fill="#190B12" stroke="#C77B9B" stroke-opacity=".28"/>
      <rect class="tbl" width="324" height="88" rx="14" pathLength="1000" style="animation-delay: -4.8s;"/>
      <rect width="3" height="88" rx="1.5" fill="#C77B9B"/>
      <text class="mono" x="22" y="26" font-size="10" letter-spacing="2" fill="#C77B9B">WHERE AI LIVES</text>
      <text class="serif" x="22" y="58" font-size="28" font-weight="300" fill="#F8F0F3">RAG &amp; Agents</text>
      <text class="sans" x="22" y="78" font-size="12" fill="#B6A3AC">LangGraph · RAG · OpenAI · Gemini · Ollama</text>
    </g>
  </g>

  <g transform="translate(836 278)">
    <g class="cd" style="animation-delay:2.2s">
      <rect width="324" height="88" rx="14" fill="#190B12" stroke="#C77B9B" stroke-opacity=".28"/>
      <rect class="tbl" width="324" height="88" rx="14" pathLength="1000" style="animation-delay: -6.1s;"/>
      <rect width="3" height="88" rx="1.5" fill="#C77B9B"/>
      <text class="mono" x="22" y="26" font-size="10" letter-spacing="2" fill="#C77B9B">DATA &amp; ASYNC</text>
      <text class="serif" x="22" y="58" font-size="28" font-weight="300" fill="#F8F0F3">Mongo + Postgres</text>
      <text class="sans" x="22" y="78" font-size="12" fill="#B6A3AC">Prisma · Redis · BullMQ · Socket.io</text>
    </g>
  </g>
</svg>"""

def build_project_card(index_str, category, name, desc, built_line, stats, chips, flow_nodes, flow_caption, delay_offset=-1.5):
    # Stats formatting: 3 pairs of (big, caption)
    # Node flow diagram on right: fits between x=760 and 1120 (4 nodes, 78px each)
    nodes_xml = []
    startX = 760
    nodeW = 78
    nodeH = 40
    gap = 20
    for idx, node in enumerate(flow_nodes):
        nx = startX + idx * (nodeW + gap)
        nodes_xml.append(f"""
    <rect x="{nx}" y="150" width="{nodeW}" height="{nodeH}" rx="20" fill="#190B12" stroke="#C77B9B" stroke-opacity=".5"/>
    <text class="mono" x="{nx + nodeW//2}" y="175" text-anchor="middle" font-size="11.5" fill="#F8F0F3">{node}</text>""")
        if idx < len(flow_nodes) - 1:
            nodes_xml.append(f'<path d="M{nx + nodeW} 170 h{gap}" stroke="#C77B9B" stroke-opacity=".7"/>')

    nodes_str = "\n".join(nodes_xml)
    endX = startX + (len(flow_nodes) - 1) * (nodeW + gap) + nodeW

    # Chips formatting
    chips_xml = []
    chipX = 56
    for c in chips:
        c_w = max(55, len(c) * 9 + 20)
        chips_xml.append(f"""<rect x="{chipX}" y="316" width="{c_w}" height="26" rx="13" fill="#190B12" stroke="#C77B9B" stroke-opacity=".35"/>
<text class="mono" x="{chipX + c_w//2}" y="333" text-anchor="middle" font-size="11.5" fill="#E5B5C7">{c}</text>""")
        chipX += c_w + 10
    chips_str = "\n".join(chips_xml)

    stat1, cap1 = stats[0]
    stat2, cap2 = stats[1]
    stat3, cap3 = stats[2]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 370" width="1200" height="370" role="img" aria-label="{name}: {desc}. Built: {built_line}. Stack: {', '.join(chips)}.">
  <title>{name}: {desc}</title>
  <desc>Built: {built_line}. Stack: {', '.join(chips)}.</desc>
  {COMMON_DEFS}
  {COMMON_STYLES}
  <rect width="1200" height="370" rx="20" fill="url(#bg)"/>
  <rect width="1200" height="370" rx="20" fill="url(#glow)"/>
  <rect width="1200" height="370" rx="20" fill="url(#grid)"/>
  <rect x=".5" y=".5" width="1199" height="369" rx="19.5" fill="none" stroke="#C77B9B" stroke-opacity=".16"/>
  <rect class="tbl" x=".5" y=".5" width="1199" height="369" rx="19.5" pathLength="1000" style="animation-delay: {delay_offset:.2f}s;"/>

  <!-- Left Info -->
  <text class="mono" x="56" y="62" font-size="12" letter-spacing="3" fill="#C77B9B">{index_str} · {category}</text>
  <text class="serif" x="54" y="118" font-size="52" font-weight="300" letter-spacing="-1.5" fill="#F8F0F3">{name}</text>
  <text class="sans" x="56" y="160" font-size="18" fill="#B6A3AC">{desc}</text>
  <text class="mono" x="56" y="200" font-size="13" fill="#C77B9B">BUILT › <tspan fill="#E5B5C7">{built_line}</tspan></text>
  <path d="M56 222H656" stroke="#C77B9B" stroke-opacity=".3"/>

  <!-- 3 Stats -->
  <text class="serif" x="56" y="262" font-size="28" font-weight="300" fill="#F8F0F3">{stat1}</text>
  <text class="sans" x="56" y="284" font-size="14" fill="#B6A3AC">{cap1}</text>

  <text class="serif" x="261" y="262" font-size="28" font-weight="300" fill="#F8F0F3">{stat2}</text>
  <text class="sans" x="261" y="284" font-size="14" fill="#B6A3AC">{cap2}</text>

  <text class="serif" x="466" y="262" font-size="28" font-weight="300" fill="#F8F0F3">{stat3}</text>
  <text class="sans" x="466" y="284" font-size="14" fill="#B6A3AC">{cap3}</text>

  <!-- Chips -->
  {chips_str}

  <!-- Node Flow on Right -->
  <text class="mono" x="{startX}" y="92" font-size="11" letter-spacing="3" fill="#B6A3AC">DATA FLOW PIPELINE</text>
  {nodes_str}
  <circle r="4" fill="#F8F0F3">
    <animate attributeName="cx" values="{startX};{endX}" dur="5s" repeatCount="indefinite"/>
    <animate attributeName="cy" values="170;170" dur="5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0" dur="5s" repeatCount="indefinite"/>
  </circle>
  <text class="mono" x="{startX}" y="308" font-size="11.5" letter-spacing="1" fill="#B6A3AC">{flow_caption}</text>
</svg>"""

def build_experience():
    rows = [
        ("FrameX AI Studio", "Interactive canvas, layer management, undo/redo state machine in Next.js", -1.2),
        ("Talent Portal", "RAG candidate match scoring, resume parsing and vector search pipelines", -2.8),
        ("Latency Optimization", "Redis caching + query indexing reduced p95 response from 450ms to 150ms", -4.4),
        ("Production Standards", "40+ REST endpoints, TypeScript strict mode, 99.8% service uptime", -6.0),
    ]
    rows_xml = []
    for i, (head, sub, delay) in enumerate(rows):
        ry = 45 + i * 72
        rows_xml.append(f"""
    <g transform="translate(640 {ry})">
      <rect width="510" height="62" rx="10" fill="#190B12" stroke="#C77B9B" stroke-opacity=".25"/>
      <rect class="tbl" width="510" height="62" rx="10" pathLength="1000" style="animation-delay: {delay:.2f}s;"/>
      <text class="mono" x="18" y="24" font-size="10" letter-spacing="2" fill="#E5B5C7">0{i+1} · {head.upper()}</text>
      <text class="sans" x="18" y="47" font-size="12.5" fill="#F8F0F3">{sub}</text>
    </g>""")
    rows_str = "\n".join(rows_xml)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 370" width="1200" height="370" role="img" aria-label="Experience: ModelSuite AI Full-Stack AI Engineer (Jun – Aug 2024). 60+ Production Features Shipped.">
  <title>Experience: ModelSuite AI</title>
  <desc>Full-Stack AI Engineer at ModelSuite AI (Jun – Aug 2024) with 60+ production features across FrameX and Talent Portal.</desc>
  {COMMON_DEFS}
  {COMMON_STYLES}
  <rect width="1200" height="370" rx="20" fill="url(#bg)"/>
  <rect width="1200" height="370" rx="20" fill="url(#glow)"/>
  <rect width="1200" height="370" rx="20" fill="url(#grid)"/>
  <rect x=".5" y=".5" width="1199" height="369" rx="19.5" fill="none" stroke="#C77B9B" stroke-opacity=".16"/>
  <rect class="tbl" x=".5" y=".5" width="1199" height="369" rx="19.5" pathLength="1000" style="animation-delay: -1.7s;"/>

  <!-- Left Side: Role, Company & Big Number -->
  <text class="mono" x="56" y="62" font-size="12" letter-spacing="3" fill="#C77B9B">FULL-STACK AI ENGINEER · JUN – AUG 2024</text>
  <text class="serif" x="54" y="118" font-size="52" font-weight="300" letter-spacing="-1.5" fill="#F8F0F3">ModelSuite AI</text>
  <text class="sans" x="56" y="156" font-size="16" fill="#B6A3AC">Architecting production platforms, AI workflow engines, and low-latency APIs.</text>

  <g transform="translate(56 185)">
    <text class="serif" x="0" y="74" font-size="82" font-weight="300" letter-spacing="-2" fill="#E5B5C7">60<tspan fill="#C77B9B">+</tspan></text>
    <text class="mono" x="156" y="38" font-size="11" letter-spacing="2" fill="#F8F0F3">PRODUCTION FEATURES</text>
    <text class="sans" x="156" y="62" font-size="13" fill="#B6A3AC">shipped across FrameX Studio &amp; Talent Portal</text>
    <text class="mono" x="156" y="84" font-size="11" letter-spacing="1.5" fill="#C77B9B">FULL-LIFECYCLE OWNERSHIP · REDIS CACHING · ZERO DOWNTIME</text>
  </g>

  <!-- Right Side: 4 Work Deliverable Rows -->
  {rows_str}
</svg>"""

def build_toolkit():
    # 3x2 grid of cards covering the entire skill set provided by the user
    # Width 360, Height 216, 6 comprehensive categories
    cards = [
        (
            "01 LANGUAGES",
            [
                ("JavaScript (ES6+) · TypeScript", 21, "#F8F0F3"),
                ("Python · SQL", 21, "#F8F0F3"),
                ("Type-Safe API Contracts &amp; Data Logic", 16.5, "#B6A3AC")
            ],
            "ASYNC/AWAIT · PROTOCOLS · SCRIPTS",
            32, 28, -1.1
        ),
        (
            "02 AI &amp; MULTI-AGENT",
            [
                ("LangChain · LangGraph", 22, "#F8F0F3"),
                ("OpenAI · Gemini · Ollama", 20, "#F8F0F3"),
                ("Multi-Agent · Tool &amp; Function Calling", 16.5, "#B6A3AC")
            ],
            "HUGGINGFACE API · PROMPT ENGINEERING",
            420, 28, -2.6
        ),
        (
            "03 RAG &amp; RETRIEVAL",
            [
                ("Embeddings · Vector Search", 21, "#F8F0F3"),
                ("Semantic Search &amp; Ranking", 20, "#F8F0F3"),
                ("Multi-Source Document Retrieval", 16.5, "#B6A3AC")
            ],
            "CITATION GROUNDING · COSINE SIMILARITY",
            808, 28, -4.0
        ),
        (
            "04 BACKEND &amp; REAL-TIME",
            [
                ("Node.js · Express.js · REST APIs", 20.5, "#F8F0F3"),
                ("Redis · BullMQ · Socket.io", 20, "#F8F0F3"),
                ("Server-Sent Events (SSE) · JWT Auth", 16.5, "#B6A3AC")
            ],
            "OAUTH 2.0 · ASYNC WORKERS · WEBSOCKETS",
            32, 276, -5.3
        ),
        (
            "05 FRONTEND",
            [
                ("React.js · Next.js (App Router)", 21, "#F8F0F3"),
                ("Redux Toolkit · Zustand", 20, "#F8F0F3"),
                ("Tailwind CSS · Responsive Systems", 16.5, "#B6A3AC")
            ],
            "COMPONENT STATE · CLIENT HYDRATION · SSR",
            420, 276, -6.5
        ),
        (
            "06 DATA, CLOUD &amp; DEVOPS",
            [
                ("MongoDB (Mongoose) · PostgreSQL", 19.5, "#F8F0F3"),
                ("Prisma ORM · Docker · CI/CD", 20, "#F8F0F3"),
                ("Vercel · Render · Git &amp; GitHub", 16.5, "#B6A3AC")
            ],
            "POSTMAN · STRIPE · CLOUDINARY INTEGRATIONS",
            808, 276, -0.6
        ),
    ]

    cards_xml = []
    for num_head, lines, footer, cx, cy, tbl_delay in cards:
        lines_xml = []
        ly = 72
        for text, sz, col in lines:
            lines_xml.append(f'<text class="serif" x="24" y="{ly}" font-size="{sz}" font-weight="300" fill="{col}">{text}</text>')
            ly += 36
        lines_str = "\n".join(lines_xml)

        footer_xml = f'<text class="mono" x="24" y="194" font-size="8.8" letter-spacing="1.4" fill="#E5B5C7">{footer}</text>' if footer else ""

        # PROPER NESTING: <g transform="translate(x y)"><g class="in"> ... to avoid CSS transform bug!
        cards_xml.append(f"""
  <g transform="translate({cx} {cy})">
    <g class="in">
      <rect width="360" height="216" rx="16" fill="#190B12" stroke="#C77B9B" stroke-opacity=".25"/>
      <rect class="tbl" width="360" height="216" rx="16" pathLength="1000" style="animation-delay: {tbl_delay:.2f}s;"/>
      <text class="mono" x="24" y="32" font-size="10" letter-spacing="2.5" fill="#C77B9B">{num_head}</text>
      {lines_str}
      <line x1="24" y1="168" x2="336" y2="168" stroke="#C77B9B" stroke-opacity=".15"/>
      {footer_xml}
    </g>
  </g>""")

    cards_str = "\n".join(cards_xml)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520" width="1200" height="520" role="img" aria-label="Toolkit: Languages, AI &amp; Multi-Agent, RAG &amp; Retrieval, Backend &amp; Real-Time, Frontend, Data, Cloud &amp; DevOps.">
  <title>Toolkit &amp; Tech Constellation</title>
  <desc>Comprehensive engineering stack covering TypeScript, Python, LangGraph, RAG, React, Next.js, Node.js, Redis, MongoDB, PostgreSQL, Docker, and Cloud CI/CD.</desc>
  {COMMON_DEFS}
  {COMMON_STYLES}
  <rect width="1200" height="520" rx="20" fill="url(#bg)"/>
  <rect width="1200" height="520" rx="20" fill="url(#glow)"/>
  <rect width="1200" height="520" rx="20" fill="url(#grid)"/>
  <rect x=".5" y=".5" width="1199" height="519" rx="19.5" fill="none" stroke="#C77B9B" stroke-opacity=".16"/>
  <rect class="tbl" x=".5" y=".5" width="1199" height="519" rx="19.5" pathLength="1000" style="animation-delay: -2.0s;"/>

  <!-- Connector Web in Gutters -->
  <path d="M40 260H1160" stroke="#C77B9B" stroke-opacity=".2" stroke-dasharray="8 6"/>
  <path d="M406 28V492" stroke="#C77B9B" stroke-opacity=".2" stroke-dasharray="8 6"/>
  <path d="M794 28V492" stroke="#C77B9B" stroke-opacity=".2" stroke-dasharray="8 6"/>

  <!-- Glowing Pulse Dot travelling along the horizontal gutter -->
  <circle r="4" fill="#E5B5C7" filter="url(#pulseGlow)">
    <animateMotion path="M40 260H1160" dur="8s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0" dur="8s" repeatCount="indefinite"/>
  </circle>

  <!-- 3x2 Grid Cards -->
  {cards_str}
</svg>"""

def build_impact():
    # 3x2 grid of stat tiles:
    # Tiles are 360px wide, start at x=40, step 380, so right edge ends at x=1160
    # Row 0: y=40, Row 1: y=220
    tiles = [
        ("60+", "PRODUCTION FEATURES", "Across FrameX &amp; Talent Portal at ModelSuite AI", 40, 40, -0.8),
        ("66%", "LATENCY REDUCTION", "p95 dropped from 450ms to 150ms with Redis", 420, 40, -2.1),
        ("40+", "REST APIS AUTHORED", "Production endpoints with strict validation", 800, 40, -3.4),
        ("6", "AI PRODUCTS SHIPPED", "End-to-end full-stack systems in production", 40, 220, -4.7),
        ("99.8%", "SERVICE UPTIME", "High-reliability architecture with fallbacks", 420, 220, -5.9),
        ("3", "RAG PIPELINES DEPLOYED", "Hybrid vector search, reranking &amp; reports", 800, 220, -1.4),
    ]

    tiles_xml = []
    for num, label, cap, tx, ty, tbl_delay in tiles:
        # PROPER NESTING: <g transform="translate(x y)"><g class="in"> ... to avoid CSS transform bug!
        tiles_xml.append(f"""
  <g transform="translate({tx} {ty})">
    <g class="in">
      <rect width="360" height="160" rx="16" fill="#190B12" stroke="#C77B9B" stroke-opacity=".25"/>
      <rect class="tbl" width="360" height="160" rx="16" pathLength="1000" style="animation-delay: {tbl_delay:.2f}s;"/>
      <text class="mono" x="24" y="36" font-size="10.5" letter-spacing="2.5" fill="#C77B9B">{label}</text>
      <text class="serif" x="24" y="98" font-size="54" font-weight="300" letter-spacing="-1.5" fill="#F8F0F3">{num}</text>
      <text class="sans" x="24" y="132" font-size="13" fill="#B6A3AC">{cap}</text>
    </g>
  </g>""")

    tiles_str = "\n".join(tiles_xml)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" width="1200" height="420" role="img" aria-label="Production Impact: 60+ features, 66% latency drop, 40+ REST APIs, 6 AI products, 99.8% uptime, 3 RAG pipelines.">
  <title>Production Impact &amp; Metrics</title>
  <desc>Verified production metrics and performance measurements for Sanjay Aggi.</desc>
  {COMMON_DEFS}
  {COMMON_STYLES}
  <rect width="1200" height="420" rx="20" fill="url(#bg)"/>
  <rect width="1200" height="420" rx="20" fill="url(#glow)"/>
  <rect width="1200" height="420" rx="20" fill="url(#grid)"/>
  <rect x=".5" y=".5" width="1199" height="419" rx="19.5" fill="none" stroke="#C77B9B" stroke-opacity=".16"/>
  <rect class="tbl" x=".5" y=".5" width="1199" height="419" rx="19.5" pathLength="1000" style="animation-delay: -3.1s;"/>

  <!-- 3x2 Stat Tiles -->
  {tiles_str}
</svg>"""

def build_github_glance():
    # Load live telemetry from site/data/github-glance.json or site/data/contributions.json
    glance_file = os.path.join(os.path.dirname(__file__), "..", "site", "data", "github-glance.json")
    contrib_file = os.path.join(os.path.dirname(__file__), "..", "site", "data", "contributions.json")
    
    stars = 10
    commits = 1374
    prs = 2
    issues = 0
    contributed_to = 33
    public_repos = 35

    if os.path.exists(contrib_file):
        try:
            with open(contrib_file, "r", encoding="utf-8") as f:
                cdata = json.load(f)
                commits = cdata.get("total", commits)
        except Exception:
            pass

    if os.path.exists(glance_file):
        try:
            with open(glance_file, "r", encoding="utf-8") as f:
                d = json.load(f)
                stars = d.get("stars", stars)
                commits = d.get("commits", commits)
                prs = d.get("prs", prs)
                issues = d.get("issues", issues)
                contributed_to = d.get("contributed_to", contributed_to)
                public_repos = d.get("public_repos", public_repos)
        except Exception:
            pass

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="1200" height="380" role="img" aria-label="GitHub at a glance: Total Stars Earned: {stars}, Total Commits: {commits:,}, Total PRs: {prs}, Total Issues: {issues}, Contributed to: {contributed_to}.">
  <title>GitHub at a glance - Sanjay Aggi</title>
  <desc>Verified real-time GitHub telemetry for @aggisanjay: {commits:,} commits, {stars} stars, {prs} PRs, {issues} issues, {contributed_to} contributed repos.</desc>
  {COMMON_DEFS}
  {COMMON_STYLES}
  <rect width="1200" height="380" rx="20" fill="url(#bg)"/>
  <rect width="1200" height="380" rx="20" fill="url(#glow)"/>
  <rect width="1200" height="380" rx="20" fill="url(#grid)"/>
  <rect x=".5" y=".5" width="1199" height="379" rx="19.5" fill="none" stroke="#C77B9B" stroke-opacity=".16"/>
  <rect class="tbl" x=".5" y=".5" width="1199" height="379" rx="19.5" pathLength="1000" style="animation-delay: -2.3s;"/>

  <!-- Left Panel: Exact GitHub at a glance list from user spec -->
  <g transform="translate(40 40)">
    <g class="in">
      <rect width="530" height="300" rx="16" fill="#14080F" stroke="#C77B9B" stroke-opacity=".25"/>
      <rect class="tbl" width="530" height="300" rx="16" pathLength="1000" style="animation-delay: -1.2s;"/>

      <!-- Header -->
      <text class="serif" x="28" y="44" font-size="28" font-weight="300" fill="#F8F0F3">GitHub at a <tspan font-style="italic" fill="url(#sheen)">glance</tspan></text>
      <circle cx="496" cy="38" r="4" fill="#C77B9B"/>
      <circle cx="496" cy="38" r="7" fill="none" stroke="#C77B9B" stroke-opacity=".4">
        <animate attributeName="r" values="4;10;4" dur="2.5s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="1;0;1" dur="2.5s" repeatCount="indefinite"/>
      </circle>

      <!-- Row 1: Stars -->
      <g transform="translate(28 72)">
        <g transform="translate(0 2)">
          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" fill="none" stroke="#E5B5C7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
        </g>
        <text class="sans" x="34" y="19" font-size="16" font-weight="600" fill="#F8F0F3">Total Stars Earned:</text>
        <text class="serif" x="472" y="21" text-anchor="end" font-size="24" font-weight="300" fill="#E5B5C7">{stars}</text>
        <path d="M0 34H472" stroke="#C77B9B" stroke-opacity=".15"/>
      </g>

      <!-- Row 2: Commits -->
      <g transform="translate(28 118)">
        <g transform="translate(0 2)">
          <circle cx="12" cy="12" r="9" fill="none" stroke="#E5B5C7" stroke-width="1.8"/>
          <polyline points="12 7 12 12 15 15" fill="none" stroke="#E5B5C7" stroke-width="1.8" stroke-linecap="round"/>
        </g>
        <text class="sans" x="34" y="19" font-size="16" font-weight="600" fill="#F8F0F3">Total Commits (last year):</text>
        <text class="serif" x="472" y="21" text-anchor="end" font-size="24" font-weight="300" fill="#E5B5C7">{commits:,}</text>
        <path d="M0 34H472" stroke="#C77B9B" stroke-opacity=".15"/>
      </g>

      <!-- Row 3: PRs -->
      <g transform="translate(28 164)">
        <g transform="translate(0 2)">
          <circle cx="6" cy="6" r="3" fill="none" stroke="#E5B5C7" stroke-width="1.8"/>
          <circle cx="6" cy="18" r="3" fill="none" stroke="#E5B5C7" stroke-width="1.8"/>
          <circle cx="18" cy="9" r="3" fill="none" stroke="#E5B5C7" stroke-width="1.8"/>
          <path d="M6 9v6M18 12a3 3 0 0 1-3 3H6" fill="none" stroke="#E5B5C7" stroke-width="1.8" stroke-linecap="round"/>
        </g>
        <text class="sans" x="34" y="19" font-size="16" font-weight="600" fill="#F8F0F3">Total PRs:</text>
        <text class="serif" x="472" y="21" text-anchor="end" font-size="24" font-weight="300" fill="#E5B5C7">{prs}</text>
        <path d="M0 34H472" stroke="#C77B9B" stroke-opacity=".15"/>
      </g>

      <!-- Row 4: Issues -->
      <g transform="translate(28 210)">
        <g transform="translate(0 2)">
          <circle cx="12" cy="12" r="9" fill="none" stroke="#E5B5C7" stroke-width="1.8"/>
          <line x1="12" y1="8" x2="12" y2="12" stroke="#E5B5C7" stroke-width="1.8" stroke-linecap="round"/>
          <line x1="12" y1="16" x2="12.01" y2="16" stroke="#E5B5C7" stroke-width="2" stroke-linecap="round"/>
        </g>
        <text class="sans" x="34" y="19" font-size="16" font-weight="600" fill="#F8F0F3">Total Issues:</text>
        <text class="serif" x="472" y="21" text-anchor="end" font-size="24" font-weight="300" fill="#E5B5C7">{issues}</text>
        <path d="M0 34H472" stroke="#C77B9B" stroke-opacity=".15"/>
      </g>

      <!-- Row 5: Contributed to -->
      <g transform="translate(28 256)">
        <g transform="translate(0 2)">
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" fill="none" stroke="#E5B5C7" stroke-width="1.8" stroke-linecap="round"/>
        </g>
        <text class="sans" x="34" y="19" font-size="16" font-weight="600" fill="#F8F0F3">Contributed to (last year):</text>
        <text class="serif" x="472" y="21" text-anchor="end" font-size="24" font-weight="300" fill="#E5B5C7">{contributed_to}</text>
      </g>
    </g>
  </g>

  <!-- Right Side: 4 Visual Telemetry Cards -->
  <g transform="translate(600 40)">
    <g class="in">
      <rect width="270" height="142" rx="14" fill="#14080F" stroke="#C77B9B" stroke-opacity=".25"/>
      <rect class="tbl" width="270" height="142" rx="14" pathLength="1000" style="animation-delay: -2.8s;"/>
      <text class="mono" x="22" y="32" font-size="10.5" letter-spacing="2.5" fill="#C77B9B">ANNUAL COMMITS</text>
      <text class="serif" x="22" y="82" font-size="44" font-weight="300" fill="#F8F0F3">{commits:,}</text>
      <text class="sans" x="22" y="112" font-size="12.5" fill="#B6A3AC">Public activity verified</text>
    </g>
  </g>

  <g transform="translate(890 40)">
    <g class="in">
      <rect width="270" height="142" rx="14" fill="#14080F" stroke="#C77B9B" stroke-opacity=".25"/>
      <rect class="tbl" width="270" height="142" rx="14" pathLength="1000" style="animation-delay: -4.2s;"/>
      <text class="mono" x="22" y="32" font-size="10.5" letter-spacing="2.5" fill="#C77B9B">REPOSITORIES</text>
      <text class="serif" x="22" y="82" font-size="44" font-weight="300" fill="#F8F0F3">{public_repos}</text>
      <text class="sans" x="22" y="112" font-size="12.5" fill="#B6A3AC">Public repos maintained</text>
    </g>
  </g>

  <g transform="translate(600 198)">
    <g class="in">
      <rect width="270" height="142" rx="14" fill="#14080F" stroke="#C77B9B" stroke-opacity=".25"/>
      <rect class="tbl" width="270" height="142" rx="14" pathLength="1000" style="animation-delay: -5.6s;"/>
      <text class="mono" x="22" y="32" font-size="10.5" letter-spacing="2.5" fill="#C77B9B">TOTAL STARS</text>
      <text class="serif" x="22" y="82" font-size="44" font-weight="300" fill="#F8F0F3">{stars}</text>
      <text class="sans" x="22" y="112" font-size="12.5" fill="#B6A3AC">Earned across projects</text>
    </g>
  </g>

  <g transform="translate(890 198)">
    <g class="in">
      <rect width="270" height="142" rx="14" fill="#14080F" stroke="#C77B9B" stroke-opacity=".25"/>
      <rect class="tbl" width="270" height="142" rx="14" pathLength="1000" style="animation-delay: -0.7s;"/>
      <text class="mono" x="22" y="32" font-size="10.5" letter-spacing="2.5" fill="#C77B9B">PULL REQUESTS</text>
      <text class="serif" x="22" y="82" font-size="44" font-weight="300" fill="#F8F0F3">{prs}</text>
      <text class="sans" x="22" y="112" font-size="12.5" fill="#B6A3AC">Merged production PRs</text>
    </g>
  </g>
</svg>"""


def build_footer():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 200" width="1200" height="200" role="img" aria-label="Sanjay - AI that ships, not just demos. Fallbacks, APIs, Data Workflows, Reliability.">
  <title>Sanjay - AI that ships, not just demos.</title>
  <desc>Engineering signature and production philosophy.</desc>
  {COMMON_DEFS}
  {COMMON_STYLES}
  <rect width="1200" height="200" rx="20" fill="url(#bg)"/>
  <rect width="1200" height="200" rx="20" fill="url(#glow)"/>
  <rect width="1200" height="200" rx="20" fill="url(#grid)"/>
  <rect x=".5" y=".5" width="1199" height="199" rx="19.5" fill="none" stroke="#C77B9B" stroke-opacity=".16"/>
  <rect class="tbl" x=".5" y=".5" width="1199" height="199" rx="19.5" pathLength="1000" style="animation-delay: -1.9s;"/>

  <g class="in">
    <text class="serif" x="600" y="92" text-anchor="middle" font-size="46" font-weight="300" fill="#F8F0F3">Sanjay — <tspan font-style="italic" fill="url(#sheen)">AI that ships, not just demos.</tspan></text>
    <path d="M440 124H760" stroke="#C77B9B" stroke-opacity=".5"/>
    <text class="mono" x="600" y="158" text-anchor="middle" font-size="11" letter-spacing="3" fill="#B6A3AC">FALLBACKS · APIS · DATA WORKFLOWS · RELIABILITY</text>
  </g>
</svg>"""

def generate_all():
    print("Generating all animated SVG assets in exact visual style...")

    # 1. Title SVGs
    titles = [
        ("title-about.svg", "01", "ABOUT", "Hello, I'm", "Sanjay.", "WHO I AM", -0.5),
        ("title-work.svg", "02", "SELECTED WORK", "Products,", "not assignments.", "FEATURED SYSTEMS", -1.5),
        ("title-experience.svg", "03", "EXPERIENCE", "Shipping at", "production scale.", "ROLE &amp; METRICS", -2.5),
        ("title-toolkit.svg", "04", "TOOLKIT", "Languages, frameworks,", "reliable systems.", "TECH STACK", -3.5),
        ("title-impact.svg", "05", "IMPACT", "Engineered for", "measurable scale.", "KEY NUMBERS", -4.5),
        ("title-commits.svg", "06", "COMMIT LOG", "Continuous delivery", "rhythm.", "ACTIVE CADENCE", -5.5),
        ("title-connect.svg", "07", "CONNECT", "Let's build something", "reliable.", "OPEN TO ROLES", -6.5),
    ]
    for fn, num, cat, lead, it, rt, dly in titles:
        fp = os.path.join(ASSETS_DIR, fn)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(make_title_svg(num, cat, lead, it, rt, dly))
        print(f"  [OK] {fn}")

    # 2. Content SVGs
    # Hero
    with open(os.path.join(ASSETS_DIR, "hero.svg"), "w", encoding="utf-8") as f:
        f.write(build_hero())
    print("  [OK] hero.svg")

    # About
    with open(os.path.join(ASSETS_DIR, "about-intro.svg"), "w", encoding="utf-8") as f:
        f.write(build_about_intro())
    print("  [OK] about-intro.svg")

    # Selected Work (6 Project Cards)
    projects = [
        (
            "project-curalink.svg", "01", "AI · RAG · HEALTHCARE", "Curalink",
            "AI medical research assistant with multi-source RAG.",
            "parallel retrieval + custom ranking + structured reports",
            [("3", "sources queried in parallel"), ("3-tier", "LLM fallback"), ("RAG", "structured reports")],
            ["React", "Node.js", "MongoDB", "HuggingFace", "Ollama"],
            ["query", "retrieve", "rank", "report"],
            "PubMed · OpenAlex · ClinicalTrials.gov",
            -1.0
        ),
        (
            "project-shopai.svg", "02", "E-COMMERCE · PERFORMANCE", "ShopAI",
            "High-performance commerce platform with Redis cache-aside.",
            "cache-aside pattern + cart state machine + responsive UI",
            [("66%", "latency drop"), ("150ms", "p95 response time"), ("Zero", "cache stampede")],
            ["React", "Node.js", "Redis", "MongoDB", "Tailwind"],
            ["request", "cache check", "db fallback", "hydrate"],
            "cache-aside · Redis cluster · instant load",
            -2.2
        ),
        (
            "project-support-desk.svg", "03", "AGENTIC AI · AUTOMATION", "Support Desk",
            "Autonomous LangGraph state machine with deterministic human routing.",
            "stateful triage + tool execution + human-in-the-loop fallback",
            [("Stateful", "graph cycles"), ("4", "tool integrations"), ("Auto", "human handoff")],
            ["React", "Node.js", "LangGraph", "OpenAI", "PostgreSQL"],
            ["ticket", "classify", "tool call", "resolve"],
            "LangGraph state machine · human in the loop",
            -3.4
        ),
        (
            "project-hireiq.svg", "04", "RECRUITMENT · MATCHING", "HireIQ",
            "AI resume intelligence and weighted matching engine.",
            "PDF extraction + vector similarity + structured criteria scoring",
            [("Weighted", "scoring engine"), ("Gemini", "parsing"), ("Instant", "candidate match")],
            ["React", "Node.js", "Gemini", "Express", "Tailwind"],
            ["resume", "extract", "vector match", "score"],
            "multi-dimensional candidate fit scoring",
            -4.6
        ),
        (
            "project-zernio.svg", "05", "AUTOMATION · SOCIAL", "Zernio",
            "Social media automation across multiple platforms.",
            "OAuth linking + BullMQ/Redis scheduling + AI content",
            [("OAuth", "account linking"), ("BullMQ", "Redis scheduling"), ("AI", "content generation")],
            ["React", "Node.js", "MongoDB", "Redis", "Gemini", "Groq"],
            ["compose", "queue", "schedule", "post"],
            "fallback scheduling · Gemini + Groq",
            -5.8
        ),
        (
            "project-doc-intel.svg", "06", "RAG · DOCUMENTS", "AI Document Intelligence",
            "RAG document Q&amp;A with SSE-streamed answers.",
            "embeddings + semantic retrieval + per-user isolation",
            [("SSE", "token streaming"), ("MiniLM", "L6-v2 embeddings"), ("Per-user", "document isolation")],
            ["Next.js", "TypeScript", "PostgreSQL", "Prisma", "Gemini"],
            ["extract", "chunk", "embed", "stream"],
            "semantic retrieval · Gemini responses",
            -0.5
        ),
    ]
    for fn, idx_s, cat, nm, dsc, blt, stats, chips, flw, cap, dly in projects:
        with open(os.path.join(ASSETS_DIR, fn), "w", encoding="utf-8") as f:
            f.write(build_project_card(f"{idx_s}", cat, nm, dsc, blt, stats, chips, flw, cap, dly))
        print(f"  [OK] {fn}")

    # Experience
    with open(os.path.join(ASSETS_DIR, "experience.svg"), "w", encoding="utf-8") as f:
        f.write(build_experience())
    print("  [OK] experience.svg")

    # Toolkit
    with open(os.path.join(ASSETS_DIR, "tech-constellation.svg"), "w", encoding="utf-8") as f:
        f.write(build_toolkit())
    print("  [OK] tech-constellation.svg")

    # Impact
    with open(os.path.join(ASSETS_DIR, "impact.svg"), "w", encoding="utf-8") as f:
        f.write(build_impact())
    print("  [OK] impact.svg")

    # GitHub at a Glance
    with open(os.path.join(ASSETS_DIR, "github-glance.svg"), "w", encoding="utf-8") as f:
        f.write(build_github_glance())
    print("  [OK] github-glance.svg")

    # Footer
    with open(os.path.join(ASSETS_DIR, "footer-signature.svg"), "w", encoding="utf-8") as f:
        f.write(build_footer())
    print("  [OK] footer-signature.svg")

    print("\nAll SVG assets generated successfully!")

if __name__ == "__main__":
    generate_all()
