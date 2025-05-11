from PIL import Image

# Bild laden
img = Image.open("logo.jpg").convert("RGB")

# Neue Bilddaten erzeugen
pixels = img.load()
width, height = img.size

# Farbe ersetzen: Blau (30,91,174) → Weiß (255,255,255)
for x in range(width):
    for y in range(height):
        if pixels[x, y] == (30, 91, 174):
            pixels[x, y] = (255, 255, 255, 0)

# Neues Bild speichern
img.save("logo_trans.jpg")