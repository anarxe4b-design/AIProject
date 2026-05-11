"""Generate a tomato icon (favicon.ico) for the Pomodoro timer."""
import struct
import os

SIZE = 32
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "favicon.ico")


def make_pixel(x, y):
    """Return (B, G, R, A) for pixel at (x,y) in a 32x32 icon."""
    cx = cy = SIZE // 2
    r = SIZE // 2 - 1
    dx = x - cx
    dy = y - cy
    dist = (dx * dx + dy * dy) ** 0.5

    # Leaf / stem area at top
    leaf_y = SIZE // 3
    if y < leaf_y and abs(x - cx) <= 5 and y > 2:
        return (0, 180, 20, 255)  # green stem

    # Extra leaf shapes
    if y < leaf_y + 3 and abs(x - cx + 6) <= 4 and y > 3:
        return (0, 200, 30, 200)
    if y < leaf_y + 3 and abs(x - cx - 6) <= 4 and y > 3:
        return (0, 200, 30, 200)

    # Main body: red circle with slight shading
    if dist <= r - 1:
        # Highlight top-left
        highlight = max(0, min(255, 60 - dx - dy))
        return (0, min(255, 60 + highlight), min(255, 200 + highlight), 255)
    elif dist <= r:
        alpha = min(255, int(255 * (r + 1 - dist)))
        return (0, 60, 200, alpha)
    else:
        return (0, 0, 0, 0)


def create_ico():
    """Create a simple tomato favicon.ico file."""
    pixels = bytearray()
    for y in range(SIZE - 1, -1, -1):
        for x in range(SIZE):
            b, g, r, a = make_pixel(x, y)
            pixels.extend([b, g, r, a])

    # === BITMAPINFOHEADER (40 bytes) ===
    bmp = struct.pack('<I', 40)    # header size
    bmp += struct.pack('<i', SIZE)  # width
    bmp += struct.pack('<i', SIZE * 2)  # height (2x for ICO format)
    bmp += struct.pack('<H', 1)    # planes
    bmp += struct.pack('<H', 32)   # bpp
    bmp += struct.pack('<I', 0)    # compression (BI_RGB)
    bmp += struct.pack('<I', len(pixels))  # image size
    bmp += struct.pack('<i', 0)    # x pixels per meter
    bmp += struct.pack('<i', 0)    # y pixels per meter
    bmp += struct.pack('<I', 0)    # colors used
    bmp += struct.pack('<I', 0)    # colors important

    # === ICO directory entry (16 bytes) ===
    entry = struct.pack('<B', SIZE if SIZE < 256 else 0)
    entry += struct.pack('<B', SIZE if SIZE < 256 else 0)
    entry += struct.pack('<B', 0)    # color count
    entry += struct.pack('<B', 0)    # reserved
    entry += struct.pack('<H', 1)    # planes
    entry += struct.pack('<H', 32)   # bpp
    entry += struct.pack('<I', len(bmp) + len(pixels))  # data size
    entry += struct.pack('<I', 22)   # offset: 6 (header) + 16 (entry)

    # === ICO header (6 bytes) ===
    header = struct.pack('<H', 0)    # reserved
    header += struct.pack('<H', 1)   # type: ICO
    header += struct.pack('<H', 1)   # count: 1 image

    with open(OUTPUT, 'wb') as f:
        f.write(header)
        f.write(entry)
        f.write(bmp)
        f.write(pixels)

    print(f"Icon created: {OUTPUT} ({os.path.getsize(OUTPUT)} bytes)")


if __name__ == "__main__":
    create_ico()
