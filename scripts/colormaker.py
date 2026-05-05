import os
import json
from PIL import Image
from collections import Counter, defaultdict

# Carpeta donde están las imágenes de los items
IMG_FOLDER = "All_Items"
# Archivo de salida
OUT_JSON = "item_colors.json"

# Mapea un color RGB a un color básico
def rgb_to_basic_color(rgb):
    r, g, b = rgb
    # Negros, blancos y grises
    if r < 40 and g < 40 and b < 40:
        return "black"
    if r > 220 and g > 220 and b > 220:
        return "white"
    if abs(r-g) < 15 and abs(r-b) < 15 and abs(g-b) < 15:
        if r > 180:
            return "light grey"
        elif r > 100:
            return "grey"
        else:
            return "dark grey"
    # Rojos
    if r > 180 and g < 100 and b < 100:
        if r > 220:
            return "light red"
        elif r < 120:
            return "dark red"
        else:
            return "red"
    # Verdes
    if g > 180 and r < 120 and b < 120:
        if g > 220:
            return "light green"
        elif g < 150:
            return "dark green"
        else:
            return "green"
    # Azules
    if b > 180 and r < 120 and g < 120:
        if b > 220:
            return "light blue"
        elif b < 150:
            return "dark blue"
        else:
            return "blue"
    # Amarillos
    if r > 180 and g > 180 and b < 100:
        if r > 220 and g > 220:
            return "light yellow"
        elif r < 150 or g < 150:
            return "dark yellow"
        else:
            return "yellow"
    # Naranjas
    if r > 180 and 100 < g < 180 and b < 80:
        if r > 220:
            return "light orange"
        else:
            return "orange"
    # Marrones
    if 90 < r < 200 and 40 < g < 140 and b < 90:
        return "brown"
    # Rosas
    if r > 180 and g < 120 and b > 120:
        if r > 220:
            return "light pink"
        else:
            return "pink"
    # Morados
    if r > 100 and b > 100 and g < 100:
        if r > 180 or b > 180:
            return "light purple"
        else:
            return "purple"
    # Cyanes
    if g > 150 and b > 150 and r < 100:
        if g > 220 or b > 220:
            return "light cyan"
        else:
            return "cyan"
    # Verde lima
    if g > 180 and r > 120 and b < 100:
        return "lime"
    # Azul turquesa
    if b > 150 and g > 120 and r < 100:
        return "turquoise"
    # Dorado
    if r > 180 and g > 150 and 60 < b < 120:
        return "gold"
    # Plateado
    if r > 170 and g > 170 and b > 170 and r < 220 and g < 220 and b < 220:
        return "silver"
    # Otros
    return "other"

def is_almost_black(rgb, threshold=30):
    r, g, b = rgb
    return r < threshold and g < threshold and b < threshold

def get_dominant_color(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB').resize((32, 32))
        pixels = list(img.getdata())
        total_pixels = len(pixels)
        # Considera negro todo pixel muy oscuro
        blackish_pixels = [p for p in pixels if is_almost_black(p)]
        non_blackish_pixels = [p for p in pixels if not is_almost_black(p)]
        # Si la mayoría son negros/casi negros, es negro
        if len(blackish_pixels) > total_pixels * 0.8:
            return (0, 0, 0)
        # Si hay suficientes colores, ignora los negros/casi negros
        if non_blackish_pixels:
            most_common = Counter(non_blackish_pixels).most_common(1)[0][0]
            return most_common
        # Si solo hay negro/casi negro
        return (0, 0, 0)

# Agrupa por color
color_groups = defaultdict(list)
for fname in os.listdir(IMG_FOLDER):
    if fname.startswith("item_") and fname.endswith(".png"):
        item_id = fname.split("_")[1].split(".")[0]
        img_path = os.path.join(IMG_FOLDER, fname)
        dom_color = get_dominant_color(img_path)
        basic_color = rgb_to_basic_color(dom_color)
        color_groups[basic_color].append(item_id)

# Ordena los ids dentro de cada color
result = {color: sorted(ids, key=lambda x: int(x)) for color, ids in color_groups.items()}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print(f"Generado {OUT_JSON} con {sum(len(ids) for ids in result.values())} items.")