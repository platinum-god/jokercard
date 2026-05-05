import json
from bs4 import BeautifulSoup

# Cargar items.json
with open('items.json', encoding='utf-8') as f:
    items = json.load(f)

# Cargar plat.html
with open('plat.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Indexar items del HTML por nombre
html_items = {}
for li in soup.select('.allitems li.textbox'):
    span = li.find('span')
    if not span:
        continue
    name_tag = span.find('p', class_='item-title')
    if not name_tag:
        continue
    name = name_tag.get_text(strip=True)
    # Descripción: todos los <p> sin clase
    description = [p.get_text(strip=True) for p in span.find_all('p', class_=False)]
    # Unlock SOLO si hay <p class="r-unlock">
    unlock_tag = span.find('p', class_='r-unlock')
    unlock = unlock_tag.get_text(strip=True) if unlock_tag else ""
    # Tags
    tags_tag = span.find('p', class_='tags')
    tags = tags_tag.get_text(strip=True) if tags_tag else ""
    # Buscar <ul> y extraer tipos y pools
    type_list = []
    item_pool = []
    ul = span.find('ul')
    if ul:
        for p in ul.find_all('p'):
            text = p.get_text(strip=True)
            if text.startswith("Type:"):
                tipos = text.replace("Type:", "").split(",")
                type_list.extend([t.strip() for t in tipos if t.strip()])
            if text.startswith("Item Pool:"):
                pools = text.replace("Item Pool:", "").split(",")
                item_pool.extend([p.strip() for p in pools if p.strip()])
    html_items[name] = {
        'description': description,
        'unlock': unlock,
        'tags': tags,
        'type_list': type_list,
        'item_pool': item_pool
    }

# Actualizar items.json
for item in items:
    name = item.get('name')
    if name in html_items:
        # Añadir descripción
        item['description'] = html_items[name]['description']
        # Añadir unlock solo si existe y no está vacío
        if html_items[name]['unlock']:
            item['unlock'] = html_items[name]['unlock']
        elif 'unlock' in item:
            del item['unlock']
        # Añadir tags
        item['tags'] = html_items[name]['tags']
        # Añadir type_list y item_pool
        item['type_list'] = html_items[name]['type_list']
        item['item_pool'] = html_items[name]['item_pool']

# Guardar resultado
with open('items_actualizado.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, indent=2, ensure_ascii=False)

print("items_actualizado.json generado con description, unlock, tags, type_list y item_pool.")