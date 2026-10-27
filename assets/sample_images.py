"""
Sample Image Generator for Multimodal Construction Intelligence Platform
Creates high-contrast, synthetic site and concrete crack images for instant 1-click testing.
"""
from PIL import Image, ImageDraw, ImageFont
import io
import math

def generate_sample_safety_image() -> bytes:
    """Generate a synthetic construction site scene with workers and scaffolding."""
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color=(135, 185, 225))  # Sky blue
    draw = ImageDraw.Draw(img)

    # Ground / Concrete Slab
    draw.rectangle([(0, 420), (width, height)], fill=(90, 95, 100))
    
    # Building structure under construction (RCC frames)
    draw.rectangle([(80, 100), (380, 420)], fill=(160, 165, 170), outline=(80, 85, 90), width=4)
    # Beams and columns
    for x in [80, 180, 280, 380]:
        draw.rectangle([(x-12, 100), (x+12, 420)], fill=(120, 125, 130))
    for y in [100, 200, 300, 400]:
        draw.rectangle([(80, y-10), (380, y+10)], fill=(110, 115, 120))

    # Scaffolding pipes (yellow/metallic)
    for x in range(420, 720, 70):
        draw.line([(x, 150), (x, 420)], fill=(230, 180, 30), width=5)
    for y in range(160, 430, 60):
        draw.line([(410, y), (730, y)], fill=(230, 180, 30), width=4)
        # Cross bracing
        draw.line([(420, y), (490, y+60)], fill=(200, 160, 30), width=2)
        draw.line([(490, y), (420, y+60)], fill=(200, 160, 30), width=2)
        draw.line([(490, y), (560, y+60)], fill=(200, 160, 30), width=2)
        draw.line([(560, y), (490, y+60)], fill=(200, 160, 30), width=2)

    # Exposed rebar hazard on ground
    for rx in range(40, 120, 15):
        draw.line([(rx, 420), (rx + 5, 360)], fill=(165, 42, 42), width=4)
        # Warning circle for un-capped rebar
        draw.ellipse([(rx-3, 355), (rx+8, 365)], outline=(255, 0, 0), width=2)

    # Worker 1: Fully Compliant (White helmet, neon-orange vest, harness, boots) on ground
    w1_x, w1_y = 230, 360
    # Head & Helmet
    draw.ellipse([(w1_x-10, w1_y-40), (w1_x+10, w1_y-20)], fill=(255, 220, 180)) # head
    draw.ellipse([(w1_x-14, w1_y-48), (w1_x+14, w1_y-34)], fill=(255, 255, 255), outline=(50, 50, 50), width=2) # Hard hat
    # High-vis vest torso
    draw.rectangle([(w1_x-15, w1_y-20), (w1_x+15, w1_y+20)], fill=(255, 102, 0)) # Neon vest
    draw.line([(w1_x-12, w1_y-15), (w1_x+12, w1_y-15)], fill=(220, 220, 220), width=3) # Reflective strip
    draw.line([(w1_x-12, w1_y+5), (w1_x+12, w1_y+5)], fill=(220, 220, 220), width=3)
    # Legs & Steel-toe boots
    draw.line([(w1_x-8, w1_y+20), (w1_x-8, w1_y+55)], fill=(30, 45, 90), width=6) # Jeans
    draw.line([(w1_x+8, w1_y+20), (w1_x+8, w1_y+55)], fill=(30, 45, 90), width=6)
    draw.rectangle([(w1_x-12, w1_y+53), (w1_x-3, w1_y+60)], fill=(40, 30, 20)) # Boots
    draw.rectangle([(w1_x+4, w1_y+53), (w1_x+13, w1_y+60)], fill=(40, 30, 20))

    # Worker 2: High elevation on scaffolding (MISSING HARNESS & HELMET - Safety Violation)
    w2_x, w2_y = 560, 230
    draw.ellipse([(w2_x-10, w2_y-40), (w2_x+10, w2_y-20)], fill=(220, 180, 140)) # head, no helmet!
    draw.rectangle([(w2_x-14, w2_y-20), (w2_x+14, w2_y+20)], fill=(30, 90, 160)) # Blue tee, NO HIGH-VIS VEST!
    draw.line([(w2_x-8, w2_y+20), (w2_x-8, w2_y+50)], fill=(50, 50, 50), width=6)
    draw.line([(w2_x+8, w2_y+20), (w2_x+8, w2_y+50)], fill=(50, 50, 50), width=6)
    # Red alert bounding box around Worker 2
    draw.rectangle([(w2_x-28, w2_y-55), (w2_x+28, w2_y+58)], outline=(255, 30, 30), width=3)

    # Banner / Watermark overlay
    draw.rectangle([(15, 15), (420, 70)], fill=(20, 30, 45))
    draw.text((25, 22), "OSHA 1926 / IS 456 SITE AUDIT PRESET", fill=(255, 200, 0))
    draw.text((25, 42), "Scenario: Scaffolding worker without harness + Ground exposed rebar", fill=(220, 230, 240))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def generate_sample_crack_image() -> bytes:
    """Generate a synthetic concrete structural shear crack image."""
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color=(185, 188, 192))  # Concrete grey
    draw = ImageDraw.Draw(img)

    # Add realistic concrete texture speckles
    import random
    random.seed(42)
    for _ in range(3500):
        sx = random.randint(0, width - 1)
        sy = random.randint(0, height - 1)
        shade = random.randint(140, 215)
        draw.point((sx, sy), fill=(shade, shade, shade))

    # Column boundary line
    draw.line([(150, 0), (150, height)], fill=(140, 145, 150), width=4)
    draw.line([(650, 0), (650, height)], fill=(140, 145, 150), width=4)

    # 45-degree Structural Shear Crack propagating through column
    crack_points = [
        (220, 480), (260, 440), (290, 410), (330, 370), (370, 340),
        (410, 300), (450, 270), (490, 220), (530, 180), (570, 130), (600, 90)
    ]
    # Main crack line (wide 2.5 - 3.5 mm structural crack)
    for i in range(len(crack_points)-1):
        p1 = crack_points[i]
        p2 = crack_points[i+1]
        draw.line([p1, p2], fill=(25, 20, 20), width=7)
        # Jittered crack edges
        draw.line([(p1[0]+2, p1[1]-1), (p2[0]+1, p2[1]+2)], fill=(45, 40, 40), width=3)
        # Secondary micro-fissures branching off
        if i in [3, 6, 8]:
            bx = p1[0] + random.randint(15, 35)
            by = p1[1] + random.randint(-20, 20)
            draw.line([p1, (bx, by)], fill=(50, 45, 45), width=2)

    # Spalling area near crack center
    spall_center = (410, 300)
    draw.ellipse([(spall_center[0]-35, spall_center[1]-25), (spall_center[0]+35, spall_center[1]+25)], fill=(130, 120, 110), outline=(80, 70, 60), width=2)
    # Exposed rebar glimpse in spalled pocket
    draw.rectangle([(spall_center[0]-18, spall_center[1]-6), (spall_center[0]+18, spall_center[1]+6)], fill=(160, 82, 45))

    # Measurement scale / Ruler overlay
    draw.rectangle([(40, 480), (160, 560)], fill=(240, 240, 240), outline=(0, 0, 0), width=2)
    draw.text((50, 490), "SCALE CALIB", fill=(0, 0, 0))
    for tick in range(50, 150, 10):
        draw.line([(tick, 520), (tick, 540)], fill=(0, 0, 0), width=2)
    draw.text((50, 542), "10mm Division", fill=(0, 0, 0))

    # Inspection banner
    draw.rectangle([(15, 15), (460, 70)], fill=(20, 30, 45))
    draw.text((25, 22), "IS 456 / ACI 224R STRUCTURAL DIAGNOSTIC PRESET", fill=(255, 90, 90))
    draw.text((25, 42), "Specimen: 45° Diagonal Shear Crack + Concrete Spalling in RCC Column", fill=(220, 230, 240))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
