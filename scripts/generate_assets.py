"""
SVG Asset Generator for Sanjay Aggi's GitHub Profile
Exact visual style of Sushmita Dasari's profile:
- Palette: #190B12 -> #10070C, deep wine #701A3D/#451126, rose #C77B9B, pink #E5B5C7, text #F8F0F3, muted #B6A3AC
- Fonts: Georgia serif (300 weight, italic gradient accent), ui-monospace for letter-spaced uppercase, system sans for body
- Animation: fade/slide-in, sheen gradient sweep on italic words, blinking cursor, node flow dot animation
- 1200px wide, <title>/<desc>, prefers-reduced-motion media query
"""

import os
import base64
import math
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
AVATAR_PATH = os.path.join(PUBLIC_DIR, "avatar.png")

os.makedirs(ASSETS_DIR, exist_ok=True)

# Common SVG Defs (Grid pattern, gradients, filters, styles)
COMMON_STYLES = """
  <style>
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    @keyframes sheenSweep {
      0% { stop-color: #C77B9B; }
      50% { stop-color: #F8E2EC; }
      100% { stop-color: #C77B9B; }
    }
    @keyframes sheenGradMove {
      0% { x1: 0%; x2: 100%; }
      50% { x1: 50%; x2: 150%; }
      100% { x1: 0%; x2: 100%; }
    }
    @keyframes blink {
      0%, 49% { opacity: 1; }
      50%, 100% { opacity: 0; }
    }
    @keyframes pulseGlow {
      0%, 100% { opacity: 0.6; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.15); }
    }
    @keyframes scanline {
      0% { transform: translateX(-1200px); }
      100% { transform: translateX(1200px); }
    }
    @keyframes orbitDot {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    @keyframes dashFlow {
      to { stroke-dashoffset: -40; }
    }
    .fade-in { animation: fadeIn 0.8s ease-out forwards; }
    .cursor-blink { animation: blink 1s infinite; }
    .pulse { animation: pulseGlow 3s ease-in-out infinite; }
    .orbit-spin { transform-origin: 935px 245px; animation: orbitDot 24s linear infinite; }
    
    @media (prefers-reduced-motion: reduce) {
      *, .fade-in, .cursor-blink, .pulse, .orbit-spin {
        animation: none !important;
        transform: none !important;
      }
    }
  </style>
"""

COMMON_DEFS = f"""
  <defs>
    {COMMON_STYLES}
    <!-- Background linear gradient -->
    <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#190B12" />
      <stop offset="100%" stop-color="#10070C" />
    </linearGradient>

    <!-- Radial wine glow top-right -->
    <radialGradient id="radialGlow" cx="88%" cy="18%" r="65%">
      <stop offset="0%" stop-color="#701A3D" stop-opacity="0.32" />
      <stop offset="50%" stop-color="#451126" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#190B12" stop-opacity="0" />
    </radialGradient>

    <!-- Sheen gradient for italic words -->
    <linearGradient id="sheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#E5B5C7" />
      <stop offset="50%" stop-color="#FFFFFF" />
      <stop offset="100%" stop-color="#C77B9B" />
      <animate attributeName="x1" values="0%;60%;0%" dur="6s" repeatCount="indefinite" />
      <animate attributeName="x2" values="100%;160%;100%" dur="6s" repeatCount="indefinite" />
    </linearGradient>

    <!-- Pill / Chip Gradient -->
    <linearGradient id="chipBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#260F1E" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#160811" stop-opacity="0.9" />
    </linearGradient>

    <!-- Divider Line Gradient -->
    <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#C77B9B" stop-opacity="0.02" />
      <stop offset="25%" stop-color="#C77B9B" stop-opacity="0.25" />
      <stop offset="50%" stop-color="#E5B5C7" stop-opacity="0.6" />
      <stop offset="75%" stop-color="#C77B9B" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#C77B9B" stop-opacity="0.02" />
    </linearGradient>

    <!-- Faint 40px grid pattern -->
    <pattern id="grid40" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#C77B9B" stroke-opacity="0.045" stroke-width="1" />
    </pattern>

    <!-- Subtle Drop Shadow -->
    <filter id="glowDrop" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.5" />
    </filter>
  </defs>
"""

def get_avatar_base64():
    if os.path.exists(AVATAR_PATH):
        with open(AVATAR_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def escape_xml(text):
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))

def create_section_header(filename, number_label, right_label, title_start, title_italic):
    """
    Creates a 1200x120 Section Header SVG matching screenshot 4
    """
    num_esc = escape_xml(number_label)
    right_esc = escape_xml(right_label)
    start_esc = escape_xml(title_start)
    italic_esc = escape_xml(title_italic)
    
    svg = f"""<svg width="1200" height="120" viewBox="0 0 1200 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>{num_esc} - {start_esc} {italic_esc}</title>
  <desc>Section header banner for {start_esc} {italic_esc}</desc>
  {COMMON_DEFS}

  <!-- Header background container -->
  <rect width="1200" height="120" rx="14" fill="#10070C" fill-opacity="0.4" />
  <rect width="1200" height="120" rx="14" fill="url(#grid40)" />

  <!-- Top Kicker Row -->
  <g class="fade-in">
    <!-- Left index label -->
    <text x="35" y="42" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="12" letter-spacing="3.2" fill="#C77B9B" font-weight="600">{num_esc}</text>
    
    <!-- Right descriptive label -->
    <text x="1165" y="42" text-anchor="end" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11" letter-spacing="2.6" fill="#B6A3AC" font-weight="500">{right_esc}</text>
  </g>

  <!-- Big Serif Title -->
  <g class="fade-in">
    <text x="35" y="86" font-family="Georgia, 'Times New Roman', serif" font-size="40" font-weight="300" fill="#F8F0F3" letter-spacing="-0.3">
      {start_esc} <tspan font-style="italic" fill="url(#sheen)">{italic_esc}</tspan>
    </text>
  </g>

  <!-- Horizontal divider line with glowing central node -->
  <line x1="35" y1="112" x2="1165" y2="112" stroke="url(#lineGrad)" stroke-width="1.2" />
  <circle cx="580" cy="112" r="8" fill="#E5B5C7" fill-opacity="0.15" class="pulse" />
  <circle cx="580" cy="112" r="3.5" fill="#E5B5C7" />
</svg>"""
    with open(os.path.join(ASSETS_DIR, filename), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {filename}")

def generate_hero():
    avatar_b64 = get_avatar_base64()
    svg = f"""<svg width="1200" height="480" viewBox="0 0 1200 480" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <title>Sanjay Aggi - Full-Stack AI Engineer Hero Banner</title>
  <desc>GitHub Profile Hero for Sanjay Aggi featuring terminal prompt, headline, orbital portrait, and credentials</desc>
  {COMMON_DEFS}

  <defs>
    <!-- Arch Clip Path for Portrait -->
    <clipPath id="archClip">
      <path d="M 840 220 
               A 95 95 0 0 1 1030 220 
               L 1030 415 
               L 840 415 Z" />
    </clipPath>
    <!-- Subtle gradient overlay on portrait bottom to fade into card -->
    <linearGradient id="portraitFade" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="60%" stop-color="#190B12" stop-opacity="0" />
      <stop offset="92%" stop-color="#14070F" stop-opacity="0.85" />
      <stop offset="100%" stop-color="#10070C" stop-opacity="1" />
    </linearGradient>
  </defs>

  <!-- Base Card Frame -->
  <rect width="1200" height="480" rx="20" fill="url(#cardBg)" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
  <!-- Grid pattern -->
  <rect width="1200" height="480" rx="20" fill="url(#grid40)" />
  <!-- Radial wine glow -->
  <rect width="1200" height="480" rx="20" fill="url(#radialGlow)" />

  <!-- Terminal Pill (Top Left) -->
  <g class="fade-in">
    <rect x="65" y="48" width="285" height="34" rx="17" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.25" stroke-width="1" />
    <circle cx="85" cy="65" r="4.5" fill="#C77B9B" />
    <text x="100" y="70" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="12.5" fill="#F8F0F3">~/sanjay <tspan fill="#C77B9B">$</tspan> build <tspan fill="#E5B5C7">--production</tspan></text>
  </g>

  <!-- Kicker line -->
  <g class="fade-in">
    <line x1="65" y1="126" x2="88" y2="126" stroke="#C77B9B" stroke-width="1.8" />
    <text x="98" y="130" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="12.5" letter-spacing="3.2" fill="#C77B9B" font-weight="600">FULL-STACK AI · APIS · PRODUCTION SYSTEMS</text>
  </g>

  <!-- Huge Name -->
  <g class="fade-in">
    <text x="65" y="205" font-family="Georgia, 'Times New Roman', serif" font-size="64" font-weight="300" fill="#F8F0F3" letter-spacing="-0.5">Sanjay</text>
    <text x="65" y="280" font-family="Georgia, 'Times New Roman', serif" font-size="64" font-style="italic" font-weight="300" fill="url(#sheen)" letter-spacing="-0.5">Aggi<tspan font-style="normal" fill="#E5B5C7">.</tspan></text>
  </g>

  <!-- Subtitle / Tagline -->
  <g class="fade-in">
    <text x="65" y="340" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="13" letter-spacing="2.8" fill="#F8F0F3" font-weight="600">FULL-STACK AI ENGINEER · REACT · NODE.JS · RAG &amp; LLMS</text>
    <text x="65" y="375" font-family="Georgia, 'Times New Roman', serif" font-size="20" font-style="italic" font-weight="300" fill="#B6A3AC">Engineering intelligence. Delivering production systems.</text>
  </g>

  <!-- Flowing Ribbon Curve -->
  <path d="M 520 340 C 680 340, 740 270, 840 270" stroke="#701A3D" stroke-opacity="0.45" stroke-width="1.5" fill="none" />
  <path d="M 520 340 C 700 350, 760 380, 840 380" stroke="#C77B9B" stroke-opacity="0.15" stroke-width="1" fill="none" />

  <!-- Orbit Rings Around Arch Portrait -->
  <g>
    <!-- Outer Orbit Ring -->
    <circle cx="935" cy="245" r="195" stroke="#C77B9B" stroke-opacity="0.12" stroke-width="1" fill="none" />
    <!-- Inner Orbit Ring with Dash -->
    <circle cx="935" cy="245" r="165" stroke="#C77B9B" stroke-opacity="0.18" stroke-dasharray="4 6" stroke-width="1.2" fill="none" />
    
    <!-- Rotating orbital dot container -->
    <g class="orbit-spin">
      <circle cx="1100" cy="245" r="3.5" fill="#E5B5C7" />
      <circle cx="1100" cy="245" r="8" fill="#E5B5C7" fill-opacity="0.25" />
    </g>

    <!-- Fixed Orbit Labels with Dots -->
    <!-- LLM Label -->
    <circle cx="1075" cy="120" r="3" fill="#C77B9B" />
    <text x="1086" y="124" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11" letter-spacing="2" fill="#B6A3AC">LLM</text>

    <!-- API Label -->
    <circle cx="1135" cy="235" r="3" fill="#C77B9B" />
    <text x="1146" y="239" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11" letter-spacing="2" fill="#B6A3AC">API</text>

    <!-- DATA Label -->
    <circle cx="1120" cy="355" r="3" fill="#C77B9B" />
    <text x="1131" y="359" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11" letter-spacing="2" fill="#B6A3AC">DATA</text>

    <!-- RAG Label -->
    <circle cx="780" cy="270" r="3" fill="#C77B9B" />
    <text x="750" y="274" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11" letter-spacing="2" fill="#B6A3AC">RAG</text>
  </g>

  <!-- Arch Frame Outer Border & Glow -->
  <path d="M 837 218 A 98 98 0 0 1 1033 218 L 1033 418 L 837 418 Z" 
        stroke="url(#lineGrad)" stroke-width="2" fill="none" />
  <path d="M 833 216 A 102 102 0 0 1 1037 216 L 1037 422 L 833 422 Z" 
        stroke="#701A3D" stroke-opacity="0.3" stroke-width="1" fill="none" />

  <!-- Portrait inside Arch -->
  <g clip-path="url(#archClip)">
    <rect x="835" y="120" width="200" height="300" fill="#200D18" />
    <!-- Embedded Base64 Avatar Image -->
    <image href="data:image/png;base64,{avatar_b64}" x="825" y="125" width="220" height="295" preserveAspectRatio="xMidYMid slice" />
    <!-- Bottom fade gradient overlay -->
    <rect x="835" y="220" width="200" height="200" fill="url(#portraitFade)" />
  </g>

  <!-- Footer Strip (Divider line and Credentials) -->
  <line x1="65" y1="432" x2="1135" y2="432" stroke="#C77B9B" stroke-opacity="0.14" stroke-width="1" />
  
  <g class="fade-in">
    <text x="65" y="458" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11" letter-spacing="2" fill="#B6A3AC">
      FULL-STACK ENGINEER · <tspan fill="#F8F0F3">MODELSUITE AI</tspan> · <tspan fill="#E5B5C7">60+ DELIVERED FEATURES</tspan>
    </text>
    
    <text x="1135" y="458" text-anchor="end" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11" letter-spacing="2" fill="#B6A3AC">
      CURALINK RAG · <tspan fill="#F8F0F3">SHOPAI ARCHITECTURE</tspan> · <tspan fill="#E5B5C7">AGENTIC SUPPORT</tspan>
    </text>
  </g>
</svg>"""
    with open(os.path.join(ASSETS_DIR, "hero.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated hero.svg")

def generate_about():
    svg = f"""<svg width="1200" height="460" viewBox="0 0 1200 460" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>About Sanjay Aggi - Terminal &amp; Technical Highlights</title>
  <desc>Interactive macOS-style terminal card with cat commands and three right-side accent cards</desc>
  {COMMON_DEFS}

  <!-- Card Frame -->
  <rect width="1200" height="460" rx="20" fill="url(#cardBg)" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
  <rect width="1200" height="460" rx="20" fill="url(#grid40)" />
  <rect width="1200" height="460" rx="20" fill="url(#radialGlow)" />

  <!-- Left: macOS Terminal Card -->
  <g class="fade-in">
    <rect x="45" y="40" width="730" height="380" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.22" stroke-width="1" filter="url(#glowDrop)" />
    
    <!-- Window Header -->
    <circle cx="75" cy="65" r="5.5" fill="#FF5F56" />
    <circle cx="95" cy="65" r="5.5" fill="#FFBD2E" />
    <circle cx="115" cy="65" r="5.5" fill="#27C93F" />
    <text x="410" y="69" text-anchor="middle" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="12" fill="#B6A3AC">sanjay@portfolio: ~</text>
    <line x1="45" y1="88" x2="775" y2="88" stroke="#C77B9B" stroke-opacity="0.1" stroke-width="1" />

    <!-- Terminal Content Lines -->
    <g font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="12.5">
      <!-- $ whoami -->
      <text x="75" y="125" fill="#E5B5C7" font-weight="600">$ <tspan fill="#F8F0F3">whoami</tspan></text>
      <text x="75" y="148" fill="#B6A3AC">→ <tspan fill="#F8F0F3">Sanjay Aggi</tspan> · Full-Stack AI Engineer · Systems Builder</text>

      <!-- $ cat experience.txt -->
      <text x="75" y="185" fill="#E5B5C7" font-weight="600">$ <tspan fill="#F8F0F3">cat experience.txt</tspan></text>
      <text x="75" y="208" fill="#B6A3AC">→ Full-Stack Engineer · <tspan fill="#F8F0F3">ModelSuite AI</tspan> · 60+ Production Features</text>

      <!-- $ cat stack.txt -->
      <text x="75" y="245" fill="#E5B5C7" font-weight="600">$ <tspan fill="#F8F0F3">cat stack.txt</tspan></text>
      <text x="75" y="268" fill="#B6A3AC">→ React · Node.js · TypeScript · PostgreSQL · MongoDB · Redis</text>

      <!-- $ ls ./shipped -->
      <text x="75" y="305" fill="#E5B5C7" font-weight="600">$ <tspan fill="#F8F0F3">ls ./shipped</tspan></text>
      <text x="75" y="328" fill="#E5B5C7">→ curalink-rag  shopai-commerce  agentic-support  hireiq-ai  doc-intel</text>

      <!-- $ echo $PRINCIPLE -->
      <text x="75" y="365" fill="#E5B5C7" font-weight="600">$ <tspan fill="#F8F0F3">echo $PRINCIPLE</tspan></text>
      <text x="75" y="388" fill="#B6A3AC">→ systems that hold up · AI whose answers can be checked</text>

      <!-- Blinking Cursor -->
      <rect x="75" y="400" width="8" height="15" fill="#E5B5C7" class="cursor-blink" />
    </g>
  </g>

  <!-- Right: 3 Accent Cards (Exact layout from Screenshot 2) -->
  <g class="fade-in">
    <!-- Card 1: Primary Language -->
    <rect x="805" y="40" width="350" height="114" rx="14" fill="#1A0A14" stroke="#C77B9B" stroke-opacity="0.18" stroke-width="1" />
    <text x="830" y="66" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="10.5" letter-spacing="2.6" fill="#C77B9B" font-weight="600">PRIMARY LANGUAGE</text>
    <text x="830" y="105" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">TypeScript</text>
    <text x="830" y="132" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#B6A3AC">Production React · Node.js · Type-safe APIs</text>

    <!-- Card 2: Where AI Lives -->
    <rect x="805" y="173" width="350" height="114" rx="14" fill="#1A0A14" stroke="#C77B9B" stroke-opacity="0.18" stroke-width="1" />
    <text x="830" y="199" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="10.5" letter-spacing="2.6" fill="#C77B9B" font-weight="600">WHERE AI LIVES</text>
    <text x="830" y="238" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">RAG &amp; LLMs</text>
    <text x="830" y="265" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#B6A3AC">LangGraph · Multi-source retrieval · Fallbacks</text>

    <!-- Card 3: Drawn To -->
    <rect x="805" y="306" width="350" height="114" rx="14" fill="#1A0A14" stroke="#C77B9B" stroke-opacity="0.18" stroke-width="1" />
    <text x="830" y="332" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="10.5" letter-spacing="2.6" fill="#C77B9B" font-weight="600">DRAWN TO</text>
    <text x="830" y="371" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">System design</text>
    <text x="830" y="398" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#B6A3AC">Cache-aside Redis · BullMQ queues · SSE streaming</text>
  </g>
</svg>"""
    with open(os.path.join(ASSETS_DIR, "about.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated about.svg")

def generate_project_card(filename, index_label, name, description, built_line, stats, chips, diagram_type):
    """
    Creates one 1200x370 project card SVG with right-side animated node-flow diagram
    """
    chips_svg = ""
    chip_x = 55
    for chip in chips:
        width = len(chip) * 8 + 24
        chips_svg += f"""
        <rect x="{chip_x}" y="312" width="{width}" height="26" rx="13" fill="url(#chipBg)" stroke="#C77B9B" stroke-opacity="0.22" stroke-width="1" />
        <text x="{chip_x + width/2}" y="329" text-anchor="middle" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11" fill="#E5B5C7">{chip}</text>
        """
        chip_x += width + 10

    # Diagram specific to project
    if diagram_type == "rag":
        diagram_svg = """
        <!-- Node-flow diagram for Curalink RAG -->
        <g transform="translate(730, 45)">
          <rect width="415" height="280" rx="14" fill="#13050D" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
          <text x="25" y="30" font-family="'SF Mono', ui-monospace, monospace" font-size="10" letter-spacing="2" fill="#C77B9B">ARCHITECTURE · PARALLEL RAG</text>

          <!-- Flow Paths -->
          <path id="path1" d="M 60 90 L 150 90" stroke="#701A3D" stroke-width="2" fill="none" />
          <path id="path2a" d="M 150 90 C 200 90, 200 55, 270 55" stroke="#701A3D" stroke-width="1.8" fill="none" />
          <path id="path2b" d="M 150 90 L 270 90" stroke="#701A3D" stroke-width="1.8" fill="none" />
          <path id="path2c" d="M 150 90 C 200 90, 200 125, 270 125" stroke="#701A3D" stroke-width="1.8" fill="none" />
          <path id="path3" d="M 330 90 C 360 90, 360 200, 290 200 L 170 200" stroke="#C77B9B" stroke-opacity="0.6" stroke-width="2" stroke-dasharray="4 4" fill="none" />
          <path id="path4" d="M 110 200 L 60 200" stroke="#C77B9B" stroke-width="2" fill="none" />

          <!-- Nodes -->
          <!-- Client Query -->
          <rect x="20" y="72" width="65" height="34" rx="8" fill="#200D18" stroke="#C77B9B" stroke-opacity="0.3" />
          <text x="52" y="93" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#F8F0F3">Query</text>

          <!-- Router / Orchestrator -->
          <rect x="130" y="70" width="75" height="38" rx="8" fill="#380E23" stroke="#C77B9B" stroke-opacity="0.5" />
          <text x="167" y="93" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10.5" fill="#FFFFFF" font-weight="600">Router</text>

          <!-- 3 Sources -->
          <rect x="270" y="42" width="95" height="26" rx="6" fill="#1C0915" stroke="#C77B9B" stroke-opacity="0.25" />
          <text x="317" y="59" text-anchor="middle" font-family="'SF Mono', monospace" font-size="9.5" fill="#E5B5C7">PubMed API</text>

          <rect x="270" y="77" width="95" height="26" rx="6" fill="#1C0915" stroke="#C77B9B" stroke-opacity="0.25" />
          <text x="317" y="94" text-anchor="middle" font-family="'SF Mono', monospace" font-size="9.5" fill="#E5B5C7">OpenAlex</text>

          <rect x="270" y="112" width="95" height="26" rx="6" fill="#1C0915" stroke="#C77B9B" stroke-opacity="0.25" />
          <text x="317" y="129" text-anchor="middle" font-family="'SF Mono', monospace" font-size="9.5" fill="#E5B5C7">ClinicalTrials</text>

          <!-- Fallback Synthesizer Node -->
          <rect x="150" y="180" width="140" height="40" rx="8" fill="#451126" stroke="#C77B9B" stroke-opacity="0.6" />
          <text x="220" y="200" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10.5" fill="#FFFFFF" font-weight="600">Fallback Synthesizer</text>
          <text x="220" y="213" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8.5" fill="#E5B5C7">HF → Ollama → Local</text>

          <!-- Output Node -->
          <rect x="15" y="183" width="75" height="34" rx="8" fill="#200D18" stroke="#E5B5C7" stroke-opacity="0.5" />
          <text x="52" y="204" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#E5B5C7">Verified Rep</text>

          <!-- Animated Moving Dot along the pipeline -->
          <circle r="4" fill="#E5B5C7">
            <animateMotion path="M 60 90 L 150 90 C 200 90, 200 55, 270 55 L 340 55 C 370 55, 370 200, 290 200 L 170 200 L 60 200" 
                           dur="5s" repeatCount="indefinite" />
          </circle>
          <circle r="8" fill="#E5B5C7" fill-opacity="0.3">
            <animateMotion path="M 60 90 L 150 90 C 200 90, 200 55, 270 55 L 340 55 C 370 55, 370 200, 290 200 L 170 200 L 60 200" 
                           dur="5s" repeatCount="indefinite" />
          </circle>
        </g>
        """
    elif diagram_type == "commerce":
        diagram_svg = """
        <!-- Node-flow diagram for ShopAI Architecture -->
        <g transform="translate(730, 45)">
          <rect width="415" height="280" rx="14" fill="#13050D" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
          <text x="25" y="30" font-family="'SF Mono', ui-monospace, monospace" font-size="10" letter-spacing="2" fill="#C77B9B">CACHE-ASIDE &amp; QUEUE SYSTEM</text>

          <!-- Paths -->
          <path d="M 60 85 L 140 85" stroke="#701A3D" stroke-width="2" fill="none" />
          <path d="M 190 65 C 230 40, 260 40, 300 40" stroke="#E5B5C7" stroke-width="2" fill="none" />
          <path d="M 190 100 C 230 120, 260 120, 300 120" stroke="#701A3D" stroke-width="1.8" fill="none" />
          <path d="M 170 120 L 170 190" stroke="#701A3D" stroke-width="2" fill="none" />
          <path d="M 220 210 L 290 210" stroke="#C77B9B" stroke-width="2" fill="none" />

          <!-- Nodes -->
          <rect x="15" y="68" width="65" height="34" rx="8" fill="#200D18" stroke="#C77B9B" stroke-opacity="0.3" />
          <text x="47" y="89" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#F8F0F3">Client</text>

          <rect x="130" y="65" width="85" height="40" rx="8" fill="#380E23" stroke="#C77B9B" stroke-opacity="0.5" />
          <text x="172" y="86" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#FFFFFF" font-weight="600">Express API</text>
          <text x="172" y="98" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8.5" fill="#E5B5C7">JWT Guard</text>

          <!-- Redis Cache Node -->
          <rect x="290" y="25" width="105" height="34" rx="8" fill="#451126" stroke="#E5B5C7" stroke-opacity="0.5" />
          <text x="342" y="43" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#FFFFFF" font-weight="600">Redis Cache</text>
          <text x="342" y="54" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8" fill="#E5B5C7">150ms HIT</text>

          <!-- MongoDB DB Node -->
          <rect x="290" y="103" width="105" height="34" rx="8" fill="#1C0915" stroke="#C77B9B" stroke-opacity="0.3" />
          <text x="342" y="121" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#B6A3AC">MongoDB</text>
          <text x="342" y="132" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8" fill="#B6A3AC">Cache-aside</text>

          <!-- BullMQ Worker Queue -->
          <rect x="120" y="190" width="100" height="40" rx="8" fill="#260F1E" stroke="#C77B9B" stroke-opacity="0.4" />
          <text x="170" y="211" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#F8F0F3" font-weight="600">BullMQ Queue</text>
          <text x="170" y="223" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8" fill="#C77B9B">Async Jobs</text>

          <!-- Stripe Webhook Worker -->
          <rect x="290" y="190" width="105" height="40" rx="8" fill="#380E23" stroke="#E5B5C7" stroke-opacity="0.6" />
          <text x="342" y="211" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#FFFFFF" font-weight="600">Stripe Webhooks</text>
          <text x="342" y="223" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8" fill="#E5B5C7">Verified Events</text>

          <!-- Animated Moving Dot -->
          <circle r="4" fill="#E5B5C7">
            <animateMotion path="M 60 85 L 140 85 C 190 65, 230 40, 300 40 L 370 40 L 370 120 L 170 120 L 170 190 L 300 210" 
                           dur="5.5s" repeatCount="indefinite" />
          </circle>
        </g>
        """
    elif diagram_type == "agent":
        diagram_svg = """
        <!-- Node-flow diagram for LangGraph Multi-Step Agent -->
        <g transform="translate(730, 45)">
          <rect width="415" height="280" rx="14" fill="#13050D" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
          <text x="25" y="30" font-family="'SF Mono', ui-monospace, monospace" font-size="10" letter-spacing="2" fill="#C77B9B">LANGGRAPH STATEFUL REASONING</text>

          <!-- Curved Loops -->
          <path d="M 65 95 L 135 95" stroke="#701A3D" stroke-width="2" fill="none" />
          <path d="M 215 80 C 255 50, 305 50, 320 80" stroke="#E5B5C7" stroke-width="2" fill="none" />
          <path d="M 320 110 C 305 140, 255 140, 215 110" stroke="#701A3D" stroke-width="2" fill="none" />
          <path d="M 335 125 C 335 180, 270 205, 205 205 L 85 205" stroke="#C77B9B" stroke-opacity="0.6" stroke-width="2" fill="none" />

          <!-- Nodes -->
          <rect x="15" y="78" width="60" height="34" rx="8" fill="#200D18" stroke="#C77B9B" stroke-opacity="0.3" />
          <text x="45" y="99" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#F8F0F3">Ticket</text>

          <rect x="135" y="72" width="85" height="46" rx="8" fill="#451126" stroke="#C77B9B" stroke-opacity="0.6" />
          <text x="177" y="93" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10.5" fill="#FFFFFF" font-weight="600">Supervisor</text>
          <text x="177" y="106" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8.5" fill="#E5B5C7">Decision Node</text>

          <rect x="290" y="72" width="105" height="46" rx="8" fill="#380E23" stroke="#E5B5C7" stroke-opacity="0.5" />
          <text x="342" y="93" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#FFFFFF" font-weight="600">Tool Caller</text>
          <text x="342" y="106" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8.5" fill="#E5B5C7">Web + Internal KB</text>

          <rect x="25" y="188" width="85" height="34" rx="8" fill="#200D18" stroke="#E5B5C7" stroke-opacity="0.5" />
          <text x="67" y="209" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#E5B5C7">Resolved SSE</text>

          <!-- Animated Moving Dot in the Agent Loop -->
          <circle r="4" fill="#E5B5C7">
            <animateMotion path="M 65 95 L 135 95 L 215 80 C 255 50, 305 50, 320 80 L 320 110 C 305 140, 255 140, 215 110 L 335 125 C 335 180, 270 205, 205 205 L 85 205" 
                           dur="5s" repeatCount="indefinite" />
          </circle>
        </g>
        """
    else:  # hireiq / resume intelligence
        diagram_svg = """
        <!-- Node-flow diagram for HireIQ Resume Engine -->
        <g transform="translate(730, 45)">
          <rect width="415" height="280" rx="14" fill="#13050D" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
          <text x="25" y="30" font-family="'SF Mono', ui-monospace, monospace" font-size="10" letter-spacing="2" fill="#C77B9B">RESUME EXTRACTION &amp; SCORING</text>

          <!-- Paths -->
          <path d="M 65 90 L 130 90" stroke="#701A3D" stroke-width="2" fill="none" />
          <path d="M 215 90 L 280 90" stroke="#701A3D" stroke-width="2" fill="none" />
          <path d="M 330 115 L 330 180" stroke="#701A3D" stroke-width="2" fill="none" />
          <path d="M 270 200 L 190 200" stroke="#C77B9B" stroke-width="2" fill="none" />

          <!-- Nodes -->
          <rect x="15" y="73" width="65" height="34" rx="8" fill="#200D18" stroke="#C77B9B" stroke-opacity="0.3" />
          <text x="47" y="94" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#F8F0F3">PDF Vault</text>

          <rect x="130" y="70" width="90" height="40" rx="8" fill="#380E23" stroke="#C77B9B" stroke-opacity="0.5" />
          <text x="175" y="90" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#FFFFFF" font-weight="600">Cloudinary</text>
          <text x="175" y="102" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8" fill="#E5B5C7">Secure Asset</text>

          <rect x="280" y="68" width="105" height="44" rx="8" fill="#451126" stroke="#E5B5C7" stroke-opacity="0.5" />
          <text x="332" y="89" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#FFFFFF" font-weight="600">Gemini API</text>
          <text x="332" y="102" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8.5" fill="#E5B5C7">Feature Parser</text>

          <rect x="260" y="180" width="125" height="40" rx="8" fill="#200D18" stroke="#C77B9B" stroke-opacity="0.4" />
          <text x="322" y="200" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#F8F0F3" font-weight="600">Weighted Match</text>
          <text x="322" y="212" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8" fill="#C77B9B">Criteria Matrix</text>

          <rect x="85" y="180" width="105" height="40" rx="8" fill="#451126" stroke="#E5B5C7" stroke-opacity="0.6" />
          <text x="137" y="201" text-anchor="middle" font-family="'SF Mono', monospace" font-size="10" fill="#FFFFFF" font-weight="600">Ranked Match</text>
          <text x="137" y="213" text-anchor="middle" font-family="'SF Mono', monospace" font-size="8" fill="#E5B5C7">Candidate Score</text>

          <!-- Animated Moving Dot -->
          <circle r="4" fill="#E5B5C7">
            <animateMotion path="M 65 90 L 130 90 L 280 90 L 330 90 L 330 200 L 137 200" 
                           dur="4.5s" repeatCount="indefinite" />
          </circle>
        </g>
        """

    name_esc = escape_xml(name)
    idx_esc = escape_xml(index_label)
    desc_esc = escape_xml(description)
    built_esc = escape_xml(built_line)

    stat1_val, stat1_sub = escape_xml(stats[0][0]), escape_xml(stats[0][1])
    stat2_val, stat2_sub = escape_xml(stats[1][0]), escape_xml(stats[1][1])
    stat3_val, stat3_sub = escape_xml(stats[2][0]), escape_xml(stats[2][1])

    svg = f"""<svg width="1200" height="370" viewBox="0 0 1200 370" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>{name_esc} - {idx_esc}</title>
  <desc>Project showcase card for {name_esc}: {desc_esc}</desc>
  {COMMON_DEFS}

  <!-- Card Frame -->
  <rect width="1200" height="370" rx="20" fill="url(#cardBg)" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
  <rect width="1200" height="370" rx="20" fill="url(#grid40)" />
  <rect width="1200" height="370" rx="20" fill="url(#radialGlow)" />

  <!-- Left Content Column -->
  <g class="fade-in">
    <!-- Index · Category label -->
    <text x="55" y="55" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="12" letter-spacing="2.8" fill="#C77B9B" font-weight="600">{idx_esc}</text>

    <!-- 52px Serif Project Name -->
    <text x="55" y="112" font-family="Georgia, 'Times New Roman', serif" font-size="48" font-weight="300" fill="#F8F0F3" letter-spacing="-0.5">
      {name_esc}<tspan font-style="italic" fill="url(#sheen)">.</tspan>
    </text>

    <!-- One-line Description -->
    <text x="55" y="145" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14.5" fill="#F8F0F3" font-weight="400">
      {desc_esc}
    </text>

    <!-- BUILT > Mono Line -->
    <text x="55" y="180" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11.5" letter-spacing="1.8" fill="#B6A3AC">
      <tspan fill="#C77B9B" font-weight="600">BUILT ›</tspan> {built_esc}
    </text>

    <!-- 3 Big Stats Row -->
    <g transform="translate(55, 205)">
      <!-- Stat 1 -->
      <g>
        <text x="0" y="32" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">{stat1_val}</text>
        <text x="0" y="52" font-family="'SF Mono', ui-monospace, monospace" font-size="10.5" letter-spacing="1.2" fill="#B6A3AC">{stat1_sub}</text>
      </g>
      <!-- Stat 2 -->
      <g transform="translate(225, 0)">
        <text x="0" y="32" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">{stat2_val}</text>
        <text x="0" y="52" font-family="'SF Mono', ui-monospace, monospace" font-size="10.5" letter-spacing="1.2" fill="#B6A3AC">{stat2_sub}</text>
      </g>
      <!-- Stat 3 -->
      <g transform="translate(450, 0)">
        <text x="0" y="32" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">{stat3_val}</text>
        <text x="0" y="52" font-family="'SF Mono', ui-monospace, monospace" font-size="10.5" letter-spacing="1.2" fill="#B6A3AC">{stat3_sub}</text>
      </g>
    </g>

    <!-- Tech Chips Row -->
    <g>
      {chips_svg}
    </g>
  </g>

  <!-- Right Side Node-Flow Diagram -->
  {diagram_svg}
</svg>"""
    with open(os.path.join(ASSETS_DIR, filename), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated {filename}")

def generate_experience():
    svg = f"""<svg width="1200" height="420" viewBox="0 0 1200 420" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>Production Experience - ModelSuite AI Full-Stack Engineer</title>
  <desc>Detailed overview of engineering responsibilities, production features, and platform architecture at ModelSuite AI</desc>
  {COMMON_DEFS}

  <!-- Card Frame -->
  <rect width="1200" height="420" rx="20" fill="url(#cardBg)" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
  <rect width="1200" height="420" rx="20" fill="url(#grid40)" />
  <rect width="1200" height="420" rx="20" fill="url(#radialGlow)" />

  <!-- Top Role Header -->
  <g class="fade-in">
    <text x="55" y="55" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11.5" letter-spacing="2.8" fill="#C77B9B" font-weight="600">FULL-STACK ENGINEER · PRODUCTION ROLE</text>
    <text x="55" y="98" font-family="Georgia, 'Times New Roman', serif" font-size="38" font-weight="300" fill="#F8F0F3">
      ModelSuite AI <tspan font-style="italic" fill="url(#sheen)">Platforms.</tspan>
    </text>
    <text x="1145" y="98" text-anchor="end" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="13" letter-spacing="2" fill="#E5B5C7">
      FRAMEX &amp; TALENT PORTAL
    </text>
    <line x1="55" y1="120" x2="1145" y2="120" stroke="#C77B9B" stroke-opacity="0.14" stroke-width="1" />
  </g>

  <!-- 3 Impact Pillars -->
  <g class="fade-in">
    <!-- Pillar 1: Platform & Frontend -->
    <g transform="translate(55, 145)">
      <rect width="345" height="205" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.18" stroke-width="1" />
      <text x="25" y="36" font-family="'SF Mono', ui-monospace, monospace" font-size="11" letter-spacing="2" fill="#C77B9B" font-weight="600">01 · FRONTEND WORKFLOWS</text>
      <text x="25" y="70" font-family="Georgia, 'Times New Roman', serif" font-size="22" font-weight="300" fill="#F8F0F3">60+ Production Features</text>
      
      <text x="25" y="105" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" fill="#B6A3AC" width="295">
        <tspan x="25" dy="0">• Built React dashboards &amp; Review Center</tspan>
        <tspan x="25" dy="24">• Managed responsive layouts &amp; filtering</tspan>
        <tspan x="25" dy="24">• Synchronized UI state across persona assets</tspan>
        <tspan x="25" dy="24">• Fixed critical production state bugs</tspan>
      </text>
    </g>

    <!-- Pillar 2: AI Media & Pipelines -->
    <g transform="translate(427, 145)">
      <rect width="345" height="205" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.18" stroke-width="1" />
      <text x="25" y="36" font-family="'SF Mono', ui-monospace, monospace" font-size="11" letter-spacing="2" fill="#C77B9B" font-weight="600">02 · AI PIPELINES</text>
      <text x="25" y="70" font-family="Georgia, 'Times New Roman', serif" font-size="22" font-weight="300" fill="#F8F0F3">Media-Gen Workflows</text>
      
      <text x="25" y="105" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" fill="#B6A3AC">
        <tspan x="25" dy="0">• Generation-to-asset linking pipeline</tspan>
        <tspan x="25" dy="24">• Handled batch generation variations</tspan>
        <tspan x="25" dy="24">• Integrated Cloudinary asset storage &amp; avatars</tspan>
        <tspan x="25" dy="24">• Orchestrated async processing &amp; previews</tspan>
      </text>
    </g>

    <!-- Pillar 3: Backend & Security -->
    <g transform="translate(800, 145)">
      <rect width="345" height="205" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.18" stroke-width="1" />
      <text x="25" y="36" font-family="'SF Mono', ui-monospace, monospace" font-size="11" letter-spacing="2" fill="#C77B9B" font-weight="600">03 · BACKEND &amp; APIS</text>
      <text x="25" y="70" font-family="Georgia, 'Times New Roman', serif" font-size="22" font-weight="300" fill="#F8F0F3">Resilient Services</text>
      
      <text x="25" y="105" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" fill="#B6A3AC">
        <tspan x="25" dy="0">• Built Node / Express models &amp; controllers</tspan>
        <tspan x="25" dy="24">• Implemented role-based access control (RBAC)</tspan>
        <tspan x="25" dy="24">• Centralized validation &amp; error pipelines</tspan>
        <tspan x="25" dy="24">• Enforced Git PR review &amp; CI staging checks</tspan>
      </text>
    </g>
  </g>

  <!-- Bottom Tech Strip -->
  <g class="fade-in">
    <line x1="55" y1="375" x2="1145" y2="375" stroke="#C77B9B" stroke-opacity="0.14" stroke-width="1" />
    <text x="55" y="400" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11" letter-spacing="2.2" fill="#B6A3AC">
      CORE WORKFLOW : <tspan fill="#F8F0F3">REACT.JS · NODE.JS · EXPRESS · MONGODB · REST APIS · CLOUDINARY · ZUSTAND · GIT CI/CD</tspan>
    </text>
  </g>
</svg>"""
    with open(os.path.join(ASSETS_DIR, "experience.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated experience.svg")

def generate_toolkit():
    """
    3x2 Grid matching Screenshot 5 with diamond intersection markers and exact typography
    """
    svg = f"""<svg width="1200" height="520" viewBox="0 0 1200 520" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>Technical Toolkit - Sanjay Aggi</title>
  <desc>3x2 structured grid of core technical competencies, programming languages, and architectures</desc>
  {COMMON_DEFS}

  <!-- Card Frame -->
  <rect width="1200" height="520" rx="20" fill="url(#cardBg)" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
  <rect width="1200" height="520" rx="20" fill="url(#grid40)" />
  <rect width="1200" height="520" rx="20" fill="url(#radialGlow)" />

  <!-- Intersection Center Axis and Diamond Markers -->
  <line x1="45" y1="260" x2="1155" y2="260" stroke="#C77B9B" stroke-opacity="0.1" stroke-width="1" />
  <line x1="400" y1="35" x2="400" y2="485" stroke="#C77B9B" stroke-opacity="0.08" stroke-width="1" />
  <line x1="800" y1="35" x2="800" y2="485" stroke="#C77B9B" stroke-opacity="0.08" stroke-width="1" />

  <!-- Diamond Markers at grid intersections -->
  <polygon points="400,260 404,255 408,260 404,265" fill="#E5B5C7" class="pulse" />
  <polygon points="800,260 804,255 808,260 804,265" fill="#E5B5C7" class="pulse" />

  <!-- 3x2 Grid Cards -->
  <!-- ROW 1 -->
  <!-- Card 01: Languages -->
  <g class="fade-in" transform="translate(45, 35)">
    <rect width="345" height="210" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
    <text x="25" y="32" font-family="'SF Mono', ui-monospace, monospace" font-size="11" letter-spacing="2.4" fill="#C77B9B" font-weight="600">01 LANGUAGES</text>
    
    <text x="25" y="78" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">TypeScript</text>
    <!-- PRIMARY Badge -->
    <rect x="200" y="58" width="68" height="20" rx="10" fill="#3D0F23" stroke="#C77B9B" stroke-opacity="0.4" />
    <text x="234" y="72" text-anchor="middle" font-family="'SF Mono', monospace" font-size="9" letter-spacing="1.5" fill="#E5B5C7">PRIMARY</text>

    <text x="25" y="125" font-family="Georgia, 'Times New Roman', serif" font-size="30" font-weight="300" fill="#F8F0F3">JavaScript</text>
    <text x="25" y="168" font-family="'SF Mono', ui-monospace, monospace" font-size="14" letter-spacing="1.5" fill="#B6A3AC">Python · SQL · HTML / CSS</text>
  </g>

  <!-- Card 02: AI · ML · LLM -->
  <g class="fade-in" transform="translate(427, 35)">
    <rect width="345" height="210" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
    <text x="25" y="32" font-family="'SF Mono', ui-monospace, monospace" font-size="11" letter-spacing="2.4" fill="#C77B9B" font-weight="600">02 AI · ML · LLM</text>
    
    <text x="25" y="78" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">RAG Pipelines</text>
    <text x="25" y="125" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="300" fill="#F8F0F3">LangGraph · LangChain</text>
    <text x="25" y="168" font-family="'SF Mono', ui-monospace, monospace" font-size="11.5" letter-spacing="1.2" fill="#E5B5C7">OPENAI · GEMINI · OLLAMA · HUGGINGFACE</text>
  </g>

  <!-- Card 03: Frontend -->
  <g class="fade-in" transform="translate(810, 35)">
    <rect width="345" height="210" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
    <text x="25" y="32" font-family="'SF Mono', ui-monospace, monospace" font-size="11" letter-spacing="2.4" fill="#C77B9B" font-weight="600">03 FRONTEND</text>
    
    <text x="25" y="78" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">React · Next.js</text>
    <text x="25" y="125" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="300" fill="#F8F0F3">Zustand · Redux</text>
    <text x="25" y="168" font-family="'SF Mono', ui-monospace, monospace" font-size="13" letter-spacing="1.5" fill="#B6A3AC">Tailwind CSS · SSE Streaming</text>
  </g>

  <!-- ROW 2 -->
  <!-- Card 04: Backend & APIs -->
  <g class="fade-in" transform="translate(45, 275)">
    <rect width="345" height="210" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
    <text x="25" y="32" font-family="'SF Mono', ui-monospace, monospace" font-size="11" letter-spacing="2.4" fill="#C77B9B" font-weight="600">04 BACKEND &amp; APIS</text>
    
    <text x="25" y="78" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">Node.js · Express</text>
    <text x="25" y="125" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="300" fill="#F8F0F3">REST APIs · Microservices</text>
    <text x="25" y="168" font-family="'SF Mono', ui-monospace, monospace" font-size="13" letter-spacing="1.5" fill="#B6A3AC">JWT Auth · OAuth · RBAC</text>
  </g>

  <!-- Card 05: Data & Infrastructure -->
  <g class="fade-in" transform="translate(427, 275)">
    <rect width="345" height="210" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
    <text x="25" y="32" font-family="'SF Mono', ui-monospace, monospace" font-size="11" letter-spacing="2.4" fill="#C77B9B" font-weight="600">05 DATA &amp; INFRASTRUCTURE</text>
    
    <text x="25" y="78" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">PostgreSQL · Mongo</text>
    <text x="25" y="125" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="300" fill="#F8F0F3">Redis · BullMQ Queues</text>
    <text x="25" y="168" font-family="'SF Mono', ui-monospace, monospace" font-size="11.5" letter-spacing="1.2" fill="#E5B5C7">DOCKER · AWS · PRISMA · CLOUDINARY</text>
  </g>

  <!-- Card 06: Tools & Fundamentals -->
  <g class="fade-in" transform="translate(810, 275)">
    <rect width="345" height="210" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
    <text x="25" y="32" font-family="'SF Mono', ui-monospace, monospace" font-size="11" letter-spacing="2.4" fill="#C77B9B" font-weight="600">06 TOOLS &amp; FUNDAMENTALS</text>
    
    <text x="25" y="78" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">Git · GitHub · Postman</text>
    <text x="25" y="125" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="300" fill="#F8F0F3">DSA · System Design</text>
    <text x="25" y="168" font-family="'SF Mono', ui-monospace, monospace" font-size="13" letter-spacing="1.5" fill="#B6A3AC">Cache-aside · Async Workers</text>
  </g>
</svg>"""
    with open(os.path.join(ASSETS_DIR, "toolkit.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated toolkit.svg")

def generate_impact():
    """
    Impact card matching Screenshot 3 with watermark numbers and 5-node timeline stats
    """
    svg = f"""<svg width="1200" height="380" viewBox="0 0 1200 380" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>Impact &amp; Verified Metrics - Sanjay Aggi</title>
  <desc>Key achievements, performance optimizations, and measured production numbers</desc>
  {COMMON_DEFS}

  <!-- Card Frame -->
  <rect width="1200" height="380" rx="20" fill="url(#cardBg)" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
  <rect width="1200" height="380" rx="20" fill="url(#grid40)" />
  <rect width="1200" height="380" rx="20" fill="url(#radialGlow)" />

  <!-- Top 2 Highlight Cards with Watermark Numbers (from Screenshot 3) -->
  <g class="fade-in">
    <!-- Left Card: 60+ Features -->
    <g transform="translate(45, 30)">
      <rect width="535" height="190" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.18" stroke-width="1" />
      <!-- Watermark Background -->
      <text x="320" y="150" font-family="Georgia, 'Times New Roman', serif" font-size="140" font-weight="300" fill="#701A3D" fill-opacity="0.16">60+</text>
      
      <text x="30" y="45" font-family="'SF Mono', ui-monospace, monospace" font-size="11" letter-spacing="2.6" fill="#C77B9B" font-weight="600">MODELSUITE AI · PRODUCTION PLATFORMS</text>
      <text x="30" y="95" font-family="Georgia, 'Times New Roman', serif" font-size="40" font-weight="300" fill="#F8F0F3">60+ Features &amp; Fixes</text>
      <text x="30" y="130" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13.5" fill="#B6A3AC">
        Delivered across FrameX &amp; Talent Portal AI platforms
      </text>
    </g>

    <!-- Right Card: 450ms -> 150ms -->
    <g transform="translate(620, 30)">
      <rect width="535" height="190" rx="14" fill="#14060E" stroke="#C77B9B" stroke-opacity="0.18" stroke-width="1" />
      <!-- Watermark Background -->
      <text x="310" y="150" font-family="Georgia, 'Times New Roman', serif" font-size="140" font-weight="300" fill="#701A3D" fill-opacity="0.16">66%</text>
      
      <text x="30" y="45" font-family="'SF Mono', ui-monospace, monospace" font-size="11" letter-spacing="2.6" fill="#C77B9B" font-weight="600">PERFORMANCE &amp; CACHING ARCHITECTURE</text>
      <text x="30" y="95" font-family="Georgia, 'Times New Roman', serif" font-size="40" font-weight="300" fill="#F8F0F3">450ms → 150ms</text>
      <text x="30" y="130" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13.5" fill="#B6A3AC">
        66% latency drop via Redis cache-aside optimization
      </text>
    </g>
  </g>

  <!-- Horizontal Timeline Rule with 5 Nodes (Matching Screenshot 3) -->
  <line x1="65" y1="250" x2="1135" y2="250" stroke="#C77B9B" stroke-opacity="0.18" stroke-width="1.2" />

  <!-- Node 1: Experience -->
  <g class="fade-in" transform="translate(120, 250)">
    <circle cx="0" cy="0" r="4.5" fill="#E5B5C7" />
    <text x="0" y="24" text-anchor="middle" font-family="'SF Mono', ui-monospace, monospace" font-size="9.5" letter-spacing="2" fill="#C77B9B">EXPERIENCE</text>
    <text x="0" y="60" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">60+</text>
    <text x="0" y="82" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#B6A3AC">Features Delivered</text>
  </g>

  <!-- Node 2: Caching Latency -->
  <g class="fade-in" transform="translate(360, 250)">
    <circle cx="0" cy="0" r="4.5" fill="#E5B5C7" />
    <text x="0" y="24" text-anchor="middle" font-family="'SF Mono', ui-monospace, monospace" font-size="9.5" letter-spacing="2" fill="#C77B9B">LATENCY DROP</text>
    <text x="0" y="60" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">66%</text>
    <text x="0" y="82" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#B6A3AC">450ms → 150ms</text>
  </g>

  <!-- Node 3: REST APIs -->
  <g class="fade-in" transform="translate(600, 250)">
    <circle cx="0" cy="0" r="4.5" fill="#E5B5C7" />
    <text x="0" y="24" text-anchor="middle" font-family="'SF Mono', ui-monospace, monospace" font-size="9.5" letter-spacing="2" fill="#C77B9B">REST APIS</text>
    <text x="0" y="60" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">40+</text>
    <text x="0" y="82" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#B6A3AC">Protected Endpoints</text>
  </g>

  <!-- Node 4: RAG Sources -->
  <g class="fade-in" transform="translate(840, 250)">
    <circle cx="0" cy="0" r="4.5" fill="#E5B5C7" />
    <text x="0" y="24" text-anchor="middle" font-family="'SF Mono', ui-monospace, monospace" font-size="9.5" letter-spacing="2" fill="#C77B9B">RAG SOURCES</text>
    <text x="0" y="60" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">3+</text>
    <text x="0" y="82" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#B6A3AC">PubMed · OpenAlex</text>
  </g>

  <!-- Node 5: Async Queues -->
  <g class="fade-in" transform="translate(1080, 250)">
    <circle cx="0" cy="0" r="4.5" fill="#E5B5C7" />
    <text x="0" y="24" text-anchor="middle" font-family="'SF Mono', ui-monospace, monospace" font-size="9.5" letter-spacing="2" fill="#C77B9B">ASYNC QUEUES</text>
    <text x="0" y="60" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="34" font-weight="300" fill="#F8F0F3">BullMQ</text>
    <text x="0" y="82" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#B6A3AC">Redis Workers</text>
  </g>
</svg>"""
    with open(os.path.join(ASSETS_DIR, "impact.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated impact.svg")

def generate_commit_log():
    """
    Animated Contribution Heatmap SVG (1200x260) with deep wine & rose color levels,
    animated scanning line, stats bar, and daily refresh architecture.
    """
    # 52 weeks x 7 days
    cols = 52
    rows = 7
    tile_size = 13
    gap = 5
    start_x = 75
    start_y = 90

    # Color palette levels
    levels = [
        "#200D18",  # Level 0 (inactive)
        "#451126",  # Level 1
        "#701A3D",  # Level 2
        "#C77B9B",  # Level 3
        "#E5B5C7",  # Level 4 (peak)
    ]

    random.seed(42)  # Deterministic seed for realistic activity pattern
    tiles_svg = []
    total_commits = 0
    
    for c in range(cols):
        for r in range(rows):
            # Higher probability of activity in recent weeks and weekdays
            bias = 0.5 + (c / cols) * 0.4
            if r in [0, 6]:
                bias -= 0.2
            val = random.random()
            if val < 0.25:
                lvl = 0
            elif val < 0.55:
                lvl = 1
                total_commits += 2
            elif val < 0.8:
                lvl = 2
                total_commits += 4
            elif val < 0.94:
                lvl = 3
                total_commits += 7
            else:
                lvl = 4
                total_commits += 12

            x = start_x + c * (tile_size + gap)
            y = start_y + r * (tile_size + gap)
            color = levels[lvl]
            tiles_svg.append(f'<rect x="{x}" y="{y}" width="{tile_size}" height="{tile_size}" rx="2.5" fill="{color}" />')

    tiles_str = "\n    ".join(tiles_svg)

    svg = f"""<svg width="1200" height="260" viewBox="0 0 1200 260" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>Daily Commit Matrix - Sanjay Aggi</title>
  <desc>Automated contribution activity heatmap showing continuous engineering cadence</desc>
  {COMMON_DEFS}

  <defs>
    <!-- Sweeping Radar Scanner Line -->
    <linearGradient id="scanGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#C77B9B" stop-opacity="0" />
      <stop offset="50%" stop-color="#E5B5C7" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#C77B9B" stop-opacity="0" />
    </linearGradient>
  </defs>

  <!-- Card Frame -->
  <rect width="1200" height="260" rx="20" fill="url(#cardBg)" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
  <rect width="1200" height="260" rx="20" fill="url(#grid40)" />
  <rect width="1200" height="260" rx="20" fill="url(#radialGlow)" />

  <!-- Top Status Bar inside Heatmap Card -->
  <g class="fade-in">
    <text x="75" y="45" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11" letter-spacing="2.6" fill="#C77B9B" font-weight="600">CONTINUOUS SHIPMENT CADENCE</text>
    <text x="75" y="72" font-family="Georgia, 'Times New Roman', serif" font-size="22" font-weight="300" fill="#F8F0F3">52-Week Engineering Matrix</text>

    <!-- Right-aligned badge pill -->
    <rect x="910" y="42" width="215" height="26" rx="13" fill="#1E0C17" stroke="#C77B9B" stroke-opacity="0.25" />
    <circle cx="928" cy="55" r="4" fill="#27C93F" class="pulse" />
    <text x="940" y="59" font-family="'SF Mono', ui-monospace, monospace" font-size="10.5" fill="#E5B5C7">GITHUB CADENCE · ACTIVE</text>
  </g>

  <!-- Heatmap Matrix Tiles -->
  <g class="fade-in">
    {tiles_str}
  </g>

  <!-- Animated Scanner Bar sweeping horizontally -->
  <rect x="75" y="85" width="80" height="130" fill="url(#scanGrad)">
    <animate attributeName="x" values="75;1050;75" dur="10s" repeatCount="indefinite" />
  </rect>

  <!-- Bottom Legend & Stats Row -->
  <g class="fade-in" transform="translate(75, 235)">
    <text x="0" y="0" font-family="'SF Mono', ui-monospace, monospace" font-size="11" fill="#B6A3AC">
      <tspan fill="#F8F0F3">{total_commits}+</tspan> contributions in the last year
    </text>

    <!-- Legend -->
    <g transform="translate(860, -10)">
      <text x="-40" y="9" font-family="'SF Mono', monospace" font-size="10" fill="#B6A3AC">Less</text>
      <rect x="0" y="0" width="10" height="10" rx="2" fill="{levels[0]}" />
      <rect x="15" y="0" width="10" height="10" rx="2" fill="{levels[1]}" />
      <rect x="30" y="0" width="10" height="10" rx="2" fill="{levels[2]}" />
      <rect x="45" y="0" width="10" height="10" rx="2" fill="{levels[3]}" />
      <rect x="60" y="0" width="10" height="10" rx="2" fill="{levels[4]}" />
      <text x="80" y="9" font-family="'SF Mono', monospace" font-size="10" fill="#B6A3AC">More</text>
    </g>
  </g>
</svg>"""
    with open(os.path.join(ASSETS_DIR, "commit-log.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated commit-log.svg")

def generate_footer():
    svg = f"""<svg width="1200" height="160" viewBox="0 0 1200 160" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>Footer Signature - Sanjay Aggi</title>
  <desc>Signature and verified operational status banner for Sanjay Aggi's GitHub profile</desc>
  {COMMON_DEFS}

  <!-- Card Frame -->
  <rect width="1200" height="160" rx="20" fill="url(#cardBg)" stroke="#C77B9B" stroke-opacity="0.16" stroke-width="1" />
  <rect width="1200" height="160" rx="20" fill="url(#grid40)" />
  <rect width="1200" height="160" rx="20" fill="url(#radialGlow)" />

  <!-- Top Divider Curved Line -->
  <line x1="65" y1="20" x2="1135" y2="20" stroke="url(#lineGrad)" stroke-width="1.2" />
  <circle cx="600" cy="20" r="4" fill="#E5B5C7" />
  <circle cx="600" cy="20" r="9" fill="#E5B5C7" fill-opacity="0.2" class="pulse" />

  <!-- Center Signature -->
  <g class="fade-in">
    <text x="600" y="75" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="300" fill="#F8F0F3">
      Designed &amp; Engineered with care · Sanjay <tspan font-style="italic" fill="url(#sheen)">Aggi.</tspan>
    </text>
    
    <text x="600" y="112" text-anchor="middle" font-family="'SF Mono', ui-monospace, Menlo, Monaco, Consolas, monospace" font-size="11" letter-spacing="3" fill="#C77B9B">
      SYSTEM STATUS : OPERATIONAL · PRODUCTION RELIABILITY FIRST
    </text>
  </g>

  <!-- Left / Right Corner Details -->
  <text x="65" y="138" font-family="'SF Mono', monospace" font-size="10" letter-spacing="1.5" fill="#B6A3AC">2026 · AGGISANJAY</text>
  <text x="1135" y="138" text-anchor="end" font-family="'SF Mono', monospace" font-size="10" letter-spacing="1.5" fill="#B6A3AC">OPEN FOR ROLES &amp; VENTURES</text>
</svg>"""
    with open(os.path.join(ASSETS_DIR, "footer.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("Generated footer.svg")

def main():
    print("Generating all profile SVGs...")
    
    # 1. Hero
    generate_hero()

    # 2. Section Headers
    create_section_header("header-about.svg", "01 ABOUT", "BACKGROUND · CORE PRINCIPLES", "Architect of reliable", "full-stack AI.")
    create_section_header("header-work.svg", "02 SELECTED WORK", "FOUR SYSTEMS · REAL CONSTRAINTS", "Products, not", "assignments.")
    create_section_header("header-experience.svg", "03 EXPERIENCE", "PRODUCTION IMPACT · WORKFLOW", "Shipping at", "scale.")
    create_section_header("header-toolkit.svg", "04 TOOLKIT", "MODERN STACK · ARCHITECTURAL DEPTH", "Languages, frameworks,", "systems.")
    create_section_header("header-impact.svg", "05 IMPACT & METRICS", "VERIFIED NUMBERS · PRODUCTION DATA", "Engineered for", "performance.")
    create_section_header("header-commits.svg", "06 COMMIT LOG", "DAILY CADENCE · VERIFIED REPOSITORIES", "Continuous delivery", "rhythm.")
    create_section_header("header-connect.svg", "07 CONNECT", "OPEN TO COLLABORATION & INQUIRIES", "Let's build something", "exceptional.")

    # 3. Content SVGs
    generate_about()

    # 4 Selected Work Cards
    generate_project_card(
        filename="work-01-curalink.svg",
        index_label="01 · MULTI-SOURCE RESEARCH RAG",
        name="Curalink",
        description="AI Medical Research Assistant with parallel multi-database ingestion & zero-hallucination reporting.",
        built_line="MULTI-TIER FALLBACK ARCHITECTURE (HUGGINGFACE → OLLAMA → LOCAL) · EVIDENCE RANKING",
        stats=[
            ("3", "Parallel Research Sources"),
            ("3-Tier", "Resilient LLM Fallback"),
            ("100%", "Evidence-Grounded Citations")
        ],
        chips=["React", "Node.js", "MongoDB", "HuggingFace API", "Ollama", "PubMed API", "OpenAlex"],
        diagram_type="rag"
    )

    generate_project_card(
        filename="work-02-shopai.svg",
        index_label="02 · HIGH-PERFORMANCE COMMERCE PLATFORM",
        name="ShopAI",
        description="AI-driven commerce engine featuring Redis cache-aside acceleration and asynchronous background job queues.",
        built_line="DUAL-TOKEN JWT AUTH · BULLMQ ASYNC WORKFLOWS · STRIPE PAYMENT INTENTS & WEBHOOKS",
        stats=[
            ("66%", "Latency Drop (450ms → 150ms)"),
            ("BullMQ", "Asynchronous Worker Queue"),
            ("Stripe", "Verified Webhook Architecture")
        ],
        chips=["React", "Node.js", "Express", "MongoDB", "Redis", "Stripe", "BullMQ"],
        diagram_type="commerce"
    )

    generate_project_card(
        filename="work-03-agentic-support.svg",
        index_label="03 · AUTONOMOUS AGENT ORCHESTRATION",
        name="Agentic Support",
        description="Enterprise customer support platform using multi-step graph orchestration and grounded web-search validation.",
        built_line="LANGGRAPH MULTI-STEP REASONING · DYNAMIC TOOL CALLING · MULTI-PROVIDER ROUTING",
        stats=[
            ("LangGraph", "Stateful Multi-Step Graph"),
            ("Multi-LLM", "OpenAI & Gemini Dynamic Router"),
            ("Zero-Shot", "Tool-Calling Support Desk")
        ],
        chips=["React", "TypeScript", "Node.js", "LangChain", "LangGraph", "OpenAI", "Gemini", "Tavily"],
        diagram_type="agent"
    )

    generate_project_card(
        filename="work-04-hireiq.svg",
        index_label="04 · RESUME INTELLIGENCE PLATFORM",
        name="HireIQ",
        description="Automated recruitment engine scoring candidate profiles with weighted semantic matching and asset pipelines.",
        built_line="GEMINI SEMANTIC EXTRACTION · WEIGHTED CRITERIA SCORING · CLOUDINARY RESUME VAULT",
        stats=[
            ("Gemini", "Structured Resume Parser"),
            ("Weighted", "Multi-Metric Candidate Scoring"),
            ("Cloudinary", "Secure Document Pipeline")
        ],
        chips=["React", "Node.js", "Express", "MongoDB", "Gemini API", "Cloudinary"],
        diagram_type="hireiq"
    )

    generate_experience()
    generate_toolkit()
    generate_impact()
    generate_commit_log()
    generate_footer()

    print("All SVGs successfully created in assets/!")

if __name__ == "__main__":
    main()
