# Erstellt die App-Symbole icon-192.png und icon-512.png für 3Room.
# Design: schwarzer Hintergrund, "3R" groß und fett, die "3" lila, das "R" weiß.
# Starten (aus dem Ordner 3Room): D:\Python\.venv\Scripts\python.exe icons_erstellen.py

from PIL import Image, ImageDraw, ImageFont

LILA = "#a855f7"
WEISS = "#ffffff"
SCHWARZ = "#000000"
SCHRIFT = "C:/Windows/Fonts/segoeuib.ttf"  # Segoe UI fett (Windows-Systemschrift)


def erstelle_icon(groesse):
    bild = Image.new("RGB", (groesse, groesse), SCHWARZ)
    zeichnen = ImageDraw.Draw(bild)
    schrift = ImageFont.truetype(SCHRIFT, int(groesse * 0.5))

    # Größe von "3R" messen, damit der Text genau in der Mitte steht
    links, oben, rechts, unten = zeichnen.textbbox((0, 0), "3R", font=schrift, anchor="ls")
    x = (groesse - (rechts - links)) / 2 - links
    y = (groesse - (unten - oben)) / 2 - oben

    # Erst die "3" in Lila, direkt dahinter das "R" in Weiß
    zeichnen.text((x, y), "3", font=schrift, fill=LILA, anchor="ls")
    zeichnen.text((x + schrift.getlength("3"), y), "R", font=schrift, fill=WEISS, anchor="ls")

    dateiname = f"icon-{groesse}.png"
    bild.save(dateiname)
    print("Gespeichert:", dateiname)


for groesse in (192, 512):
    erstelle_icon(groesse)
