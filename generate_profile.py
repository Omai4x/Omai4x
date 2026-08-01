#!/usr/bin/env python3
"""
Generate terminal-window styled GitHub profile hero cards (dark.svg + light.svg),
matching the arifhaxn reference layout (1180x610).

Edit the CONFIG block, then run:  python3 generate_profile.py
Outputs: dark.svg, light.svg
"""

import random

# ----------------------------------------------------------------------------
# CONFIG  --  edit these to your own details
# ----------------------------------------------------------------------------
CFG = {
    "prompt": "emmanuelokechukwu291@gmail.com - % ./profile.sh --live",
    "email_chip": "emmanuelokechukwu291@gmail.com",
    "aria": "Emmanuel Okechukwu — profile.sh --live",
    "system": [
        ("Subject",       "Emmanuel Okechukwu"),
        ("Role",          "Founder, NeoWeb Services"),
        ("Focus",         "Custom Web, SaaS & Web Apps"),
        ("Origin",        "Nigeria"),
        ("Status",        "Shipping production-ready software"),
        ("ToolChain",     "VS Code, Git, Figma, Vercel"),
    ],
    "core": [
        ("Core.Lang",     "TypeScript, JavaScript"),
        ("Core.Frontend", "React, Next.js, HTML/CSS"),
        ("Core.Backend",  "Node.js"),
        ("Core.Database", "PostgreSQL, MongoDB"),
        ("Core.Infra",    "Vercel, Docker, Git"),
    ],
    "contact": [
        ("Grid.Mail",     "emmanuelokechukwu291@gmail.com"),
        ("Grid.Portfolio","coming soon"),
        ("Grid.LinkedIn", "your-linkedin-handle"),
        ("Grid.GitHub",   "@Omai4x"),
        ("Grid.Company",  "NeoWeb Services"),
    ],
    "footer": "> More about me & projects below in README",
}

# ----------------------------------------------------------------------------
# Themes
# ----------------------------------------------------------------------------
THEMES = {
    "dark": {
        "outer_bg":  "#070B16",
        "bar_bg":    "#0B1222",
        "map_bg":    "#0A101F",
        "teal":      "#22D3EE",
        "violet":    "#A78BFA",
        "value":     "#F8FAFC",
        "dim":       "#94A3B8",
        "dim2":      "#475569",
        "dots":      "#334155",
        "chip_bg":   "#4C1D95",
        "chip_fg":   "#E9D5FF",
        "grad_a":    "#22D3EE",
        "grad_b":    "#A78BFA",
    },
    "light": {
        "outer_bg":  "#FFFFFF",
        "bar_bg":    "#F1F5F9",
        "map_bg":    "#F8FAFC",
        "teal":      "#0891B2",
        "violet":    "#7C3AED",
        "value":     "#0F172A",
        "dim":       "#475569",
        "dim2":      "#94A3B8",
        "dots":      "#CBD5E1",
        "chip_bg":   "#EDE9FE",
        "chip_fg":   "#6D28D9",
        "grad_a":    "#0891B2",
        "grad_b":    "#7C3AED",
    },
}

RED, YELLOW, GREEN, LIVE_RED = "#ff5f56", "#ffbd2e", "#27c93f", "#F87171"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

W, H = 1180, 610
ROW_X, ROW_LEN, ROW_END = 470, 655, 1125   # rows span x=470..1125
FS = 14
CHARS_PER_ROW = 74                          # slightly under 655px so rows stay
                                            # in-bounds even if textLength ignored


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def row(y, label, value, T, sep="."):
    """One aligned row stretched to exactly 655px via textLength."""
    ndots = max(2, CHARS_PER_ROW - len(label) - len(value) - 2)
    leader = sep * ndots
    return (
        f'<text x="{ROW_X}" y="{y}" font-size="{FS}" textLength="{ROW_LEN}" '
        f'lengthAdjust="spacingAndGlyphs" xml:space="preserve">'
        f'<tspan fill="{T["teal"]}">{esc(label)} </tspan>'
        f'<tspan fill="{T["dots"]}">{leader}</tspan>'
        f'<tspan fill="{T["value"]}"> {esc(value)}</tspan></text>'
    )


def lightning_dots(T):
    """Static violet particle field forming a lightning bolt inside the map box."""
    # bolt polygon in map-box local coords (box is 400x492)
    poly = [(230, 30), (150, 250), (215, 250), (120, 470),
            (300, 210), (225, 210), (300, 30)]

    def inside(x, y):
        n = len(poly); ins = False; j = n - 1
        for i in range(n):
            xi, yi = poly[i]; xj, yj = poly[j]
            if ((yi > y) != (yj > y)) and \
               (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                ins = not ins
            j = i
        return ins

    random.seed(11)
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    out, got, tries = [], 0, 0
    while got < 460 and tries < 40000:
        tries += 1
        x = random.uniform(min(xs) - 8, max(xs) + 8)
        y = random.uniform(min(ys) - 8, max(ys) + 8)
        if inside(x, y):
            r = random.choice([1.0, 1.3, 1.6, 2.0])
            op = random.choice([0.45, 0.65, 0.85, 1.0])
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" '
                       f'fill="{T["violet"]}" opacity="{op}"/>')
            got += 1
    return "\n".join(out)


def build(name):
    T = THEMES[name]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="{FONT}" role="img" '
         f'aria-label="{esc(CFG["aria"])}">']

    # gradient for accent border
    s.append(f'<defs><linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0" stop-color="{T["grad_a"]}"/>'
             f'<stop offset="1" stop-color="{T["grad_b"]}"/></linearGradient></defs>')

    # card body + accent border
    s.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="18" fill="{T["outer_bg"]}"/>')
    s.append(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="17" fill="none" '
             f'stroke="url(#accent)" stroke-width="1.8" opacity="0.9"/>')

    # title bar
    s.append(f'<rect x="2" y="2" width="{W-4}" height="46" rx="18" fill="{T["bar_bg"]}"/>')
    s.append(f'<rect x="2" y="30" width="{W-4}" height="18" fill="{T["bar_bg"]}"/>')
    for i, c in enumerate([RED, YELLOW, GREEN]):
        s.append(f'<circle cx="{28 + i*22}" cy="25" r="6.5" fill="{c}"/>')
    s.append(f'<text x="{W/2}" y="29" text-anchor="middle" font-size="12" '
             f'fill="{T["dim"]}">{esc(CFG["prompt"])}</text>')

    # ---- left: visual map ----
    s.append(f'<text x="38" y="74" font-size="10" letter-spacing="3" '
             f'fill="{T["dim2"]}">VISUAL.MAP</text>')
    s.append(f'<rect x="36" y="84" width="400" height="492" rx="10" '
             f'fill="{T["map_bg"]}" stroke="{T["teal"]}" stroke-width="1.5" opacity="0.9"/>')
    s.append(f'<g transform="translate(36,84)">{lightning_dots(T)}</g>')

    # ---- right: system info ----
    s.append(f'<text x="470" y="106" font-size="13" letter-spacing="2" '
             f'font-weight="700" fill="{T["teal"]}">SYSTEM.INFO</text>')
    s.append(f'<circle cx="1089" cy="102" r="4" fill="{LIVE_RED}"/>')
    s.append(f'<text x="1125" y="106" text-anchor="end" font-size="12" '
             f'font-weight="700" fill="{LIVE_RED}">LIVE</text>')

    # email chip
    chip_w = len(CFG["email_chip"]) * 8.4 + 16
    s.append(f'<rect x="470" y="122" width="{chip_w:.0f}" height="20" rx="4" fill="{T["chip_bg"]}"/>')
    s.append(f'<text x="478" y="136" font-size="13" fill="{T["chip_fg"]}">'
             f'{esc(CFG["email_chip"])}</text>')

    y = 162
    for label, value in CFG["system"]:
        s.append(row(y, label, value, T)); y += 23
    y += 8
    for label, value in CFG["core"]:
        s.append(row(y, label, value, T)); y += 23
    y += 8
    # contact separator row
    ndash = CHARS_PER_ROW - len("- Contact") - 1
    s.append(f'<text x="470" y="{y}" font-size="{FS}" textLength="{ROW_LEN}" '
             f'lengthAdjust="spacingAndGlyphs" xml:space="preserve">'
             f'<tspan fill="{T["dim"]}">- Contact </tspan>'
             f'<tspan fill="{T["dots"]}">{"-"*ndash}</tspan></text>')
    y += 23
    for label, value in CFG["contact"]:
        s.append(row(y, label, value, T)); y += 23
    y += 8
    s.append(f'<text x="470" y="{y}" font-size="13" fill="{T["dim"]}">'
             f'{esc(CFG["footer"])} <tspan fill="{T["teal"]}">&#9660;</tspan></text>')

    s.append('</svg>')
    return "\n".join(s)


if __name__ == "__main__":
    for nm in ("dark", "light"):
        with open(f"{nm}.svg", "w") as f:
            f.write(build(nm))
        print(f"wrote {nm}.svg")
