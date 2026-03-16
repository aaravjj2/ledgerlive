#!/usr/bin/env python3
"""
Generate professional Devpost thumbnail for LedgerLive
Design: Dark F1 aesthetic, 1280×720 PNG
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Dimensions
WIDTH = 1280
HEIGHT = 720

# F1-inspired color palette
BG_DARK = "#0F1724"      # Deep space blue (F1 grid background)
ACCENT_CYAN = "#00D9FF"  # Bright cyan (agent highlight)
ACCENT_RED = "#E8002D"   # F1 red (action highlight)
TEXT_WHITE = "#F5F5F5"   # Bright white
TEXT_GRAY = "#A0A0A0"    # Muted gray

# Create image with dark background
img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_DARK)
draw = ImageDraw.Draw(img, 'RGBA')

# Add subtle grid pattern (F1 aesthetic)
grid_spacing = 40
grid_color = (30, 40, 60, 20)  # Very subtle with alpha
for x in range(0, WIDTH, grid_spacing):
    draw.line([(x, 0), (x, HEIGHT)], fill=grid_color, width=1)
for y in range(0, HEIGHT, grid_spacing):
    draw.line([(0, y), (WIDTH, y)], fill=grid_color, width=1)

# Font setup
try:
    # Try to use system fonts
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except:
    # Fallback to default
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    body_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Draw glowing agent avatar (cyan circle, left side)
avatar_x = 120
avatar_y = 360
avatar_radius = 80
# Glow effect (concentric circles)
for i in range(15, 0, -1):
    alpha = int(50 * (1 - i/15))
    draw.ellipse(
        [(avatar_x - avatar_radius - i, avatar_y - avatar_radius - i),
         (avatar_x + avatar_radius + i, avatar_y + avatar_radius + i)],
        fill=(0, 217, 255, alpha)
    )
# Main circle
draw.ellipse(
    [(avatar_x - avatar_radius, avatar_y - avatar_radius),
     (avatar_x + avatar_radius, avatar_y + avatar_radius)],
    fill=ACCENT_CYAN
)
# Agent icon (simple triangle representing agent/AI)
draw.polygon(
    [(avatar_x, avatar_y - 30),
     (avatar_x - 30, avatar_y + 25),
     (avatar_x + 30, avatar_y + 25)],
    fill=BG_DARK
)

# Main title: "LedgerLive"
title_text = "LedgerLive"
title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (WIDTH - title_width) // 2
title_y = 80
draw.text((title_x, title_y), title_text, fill=TEXT_WHITE, font=title_font)

# Subtitle: "AI-Powered Financial Close"
subtitle_text = "AI-Powered Financial Close"
subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (WIDTH - subtitle_width) // 2
subtitle_y = 180
draw.text((subtitle_x, subtitle_y), subtitle_text, fill=ACCENT_CYAN, font=subtitle_font)

# Metrics section (right side)
metrics_x = 750
metrics_y = 240

# Metric 1: 60% Faster
metric1_text = "✓ 60% Faster"
draw.text((metrics_x, metrics_y), metric1_text, fill=ACCENT_RED, font=body_font)

# Metric 2: Real-Time
metric2_text = "✓ Real-Time Agents"
draw.text((metrics_x, metrics_y + 60), metric2_text, fill=ACCENT_RED, font=body_font)

# Metric 3: 99.7% Uptime
metric3_text = "✓ 99.7% Uptime"
draw.text((metrics_x, metrics_y + 120), metric3_text, fill=ACCENT_RED, font=body_font)

# Bottom banner
banner_height = 100
draw.rectangle([(0, HEIGHT - banner_height), (WIDTH, HEIGHT)], fill=(20, 30, 50, 240))

# Bottom text
bottom_text = "Gemini Live Agent Challenge"
bottom_bbox = draw.textbbox((0, 0), bottom_text, font=small_font)
bottom_width = bottom_bbox[2] - bottom_bbox[0]
bottom_x = (WIDTH - bottom_width) // 2
draw.text((bottom_x, HEIGHT - 70), bottom_text, fill=TEXT_GRAY, font=small_font)

# Corner accent: "LIVE DEMO" badge
badge_text = "LIVE DEMO"
draw.rectangle([(20, HEIGHT - 50), (200, HEIGHT - 20)], outline=ACCENT_CYAN, width=2)
draw.text((30, HEIGHT - 45), badge_text, fill=ACCENT_CYAN, font=small_font)

# Save
output_path = "/home/aarav/Aarav/ledgerlive/ledgerlive/artifacts/demo/THUMBNAIL.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
img.save(output_path, 'PNG')
print(f"✓ Thumbnail created: {output_path}")
print(f"  Resolution: {WIDTH}×{HEIGHT} px")
print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")
