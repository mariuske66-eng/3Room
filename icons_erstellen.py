# Erstellt die App-Symbole icon-192.png, icon-512.png und icon-maskable-512.png für 3Room.
# Zeichnet dieselben Formen wie icon.svg nach (Pillow kann SVG nicht öffnen).
# Hintergrund: volles schwarzes Quadrat ohne runde Ecken (Android rundet selbst ab).
# Starten (aus dem Ordner 3Room): D:\Python\.venv\Scripts\python.exe icons_erstellen.py

from PIL import Image, ImageDraw

# Formen aus icon.svg, Maße im SVG-Raster 160 x 160: (x, y, Breite, Höhe, Farbe)
STREIFEN_SONNE = [
    (30, 46, 100, 13, "#ffb000"),
    (30, 59, 100, 11, "#ff8a00"),
    (30, 70, 100, 11, "#ff5a3c"),
    (30, 81, 100, 11, "#ff2d6e"),
]
BALKEN = [
    (8, 91, 144, 5, "#5a0b99"),
    (40, 104, 80, 4, "#ff2d6e"),
    (54, 114, 52, 4, "#b3127a"),
    (68, 124, 24, 4, "#5a0b99"),
]
# Halbkreis, auf den die Sonnen-Streifen zugeschnitten werden: Mitte (80, 92), Radius 44
MITTE_X, MITTE_Y, RADIUS = 80, 92, 44

LUPE = 4  # erst 4-mal größer zeichnen, dann verkleinern: glattere Kanten

# Umriss aller Formen im SVG: links 8, rechts 152, oben 48 (Kreis-Spitze), unten 128
LOGO_BREITE = 152 - 8
LOGO_MITTE_Y = (48 + 128) / 2


def erstelle_icon(groesse, dateiname, maskable=False):
    gross = groesse * LUPE

    if maskable:
        # Logo kleiner: Es soll nur die inneren 70 % füllen (Sicherheitszone für
        # Android) und genau in der Mitte stehen.
        f = gross * 0.70 / LOGO_BREITE
        mitte_y = LOGO_MITTE_Y
    else:
        # Normal: das ganze SVG-Raster (160 x 160) füllt das Bild
        f = gross / 160
        mitte_y = 80

    # Umrechnung SVG-Punkt -> Pixel (Mitte des SVG landet in der Bildmitte)
    def px(x):
        return (x - 80) * f + gross / 2

    def py(y):
        return (y - mitte_y) * f + gross / 2

    def rechteck(x, y, b, h):
        return [px(x), py(y), px(x + b), py(y + h)]

    # 1. Schwarzer Hintergrund
    bild = Image.new("RGB", (gross, gross), "#000000")

    # 2. Sonnen-Streifen auf eigener Ebene zeichnen ...
    streifen = Image.new("RGB", (gross, gross), "#000000")
    zeichnen = ImageDraw.Draw(streifen)
    for x, y, b, h, farbe in STREIFEN_SONNE:
        zeichnen.rectangle(rechteck(x, y, b, h), fill=farbe)

    # ... und nur innerhalb des oberen Halbkreises übernehmen
    maske = Image.new("L", (gross, gross), 0)
    kreis = [px(MITTE_X - RADIUS), py(MITTE_Y - RADIUS),
             px(MITTE_X + RADIUS), py(MITTE_Y + RADIUS)]
    ImageDraw.Draw(maske).pieslice(kreis, 180, 360, fill=255)
    bild.paste(streifen, (0, 0), maske)

    # 3. Balken darüber
    zeichnen = ImageDraw.Draw(bild)
    for x, y, b, h, farbe in BALKEN:
        zeichnen.rectangle(rechteck(x, y, b, h), fill=farbe)

    # 4. Auf Zielgröße verkleinern und speichern
    bild = bild.resize((groesse, groesse), Image.LANCZOS)
    bild.save(dateiname)
    print("Gespeichert:", dateiname)


erstelle_icon(192, "icon-192.png")
erstelle_icon(512, "icon-512.png")
erstelle_icon(512, "icon-maskable-512.png", maskable=True)
