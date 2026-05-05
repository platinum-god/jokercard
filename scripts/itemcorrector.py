import json
import re

def normalize(name):
    return name.strip().lower().replace("’", "'").replace("`", "'")

# 1. Extraer pickups de plat.html
with open('plat.html', encoding='utf-8') as f:
    html = f.read()

# Usar regex para extraer nombre y pickup
item_pickups = {}
for match in re.finditer(
    r'<p class="item-title">(.*?)</p>.*?<p class="pickup">"(.*?)"</p>',
    html, re.DOTALL
):
    name = normalize(match.group(1))
    pickup = match.group(2).strip()
    item_pickups[name] = pickup

# 2. Leer items.json
with open('items.json', encoding='utf-8') as f:
    items = json.load(f)

# 3. Añadir pickup a cada item si corresponde
for item in items:
    name = normalize(item.get('name', ''))
    pickup = item_pickups.get(name)
    if pickup:
        item['pickup'] = pickup

# 4. Guardar resultado
with open('items.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)
