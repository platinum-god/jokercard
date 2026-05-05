import json
from bs4 import BeautifulSoup

def normalize(name):
    return name.strip().lower().replace("’", "'").replace("`", "'")

# Cargar items.json
with open("items.json", encoding="utf-8") as f:
    items = json.load(f)

# Cargar plat.html
with open("plat.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Crear un dict de items por nombre normalizado
items_by_name = {normalize(item.get("name", "")): item for item in items if "name" in item}

# Recorrer cada <li class="textbox">
for li in soup.select("li.textbox"):
    span = li.find("span")
    if not span:
        continue
    # Buscar el nombre del item en el primer <p class="item-title">, si existe
    title_tag = span.find("p", class_="item-title")
    if title_tag:
        item_name = normalize(title_tag.get_text())
    else:
        # Si no hay <p class="item-title">, usar la primera línea de texto del span
        lines = [line.strip() for line in span.get_text(separator="\n").splitlines() if line.strip()]
        if not lines:
            continue
        item_name = normalize(lines[0])
    # Buscar "Recharge Time:" en las líneas del span
    recharge_times = []
    for line in span.get_text(separator="\n").splitlines():
        line = line.strip()
        if line.startswith("Recharge Time:"):
            recharge_times.append(line.split("Recharge Time:", 1)[1].strip())
    # Si hay recharge_time y el item existe en el json, añadirlo
    if recharge_times and item_name in items_by_name:
        items_by_name[item_name]["recharge_time"] = recharge_times

# Guardar el resultado
with open("items.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)