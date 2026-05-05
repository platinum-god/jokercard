import json
from bs4 import BeautifulSoup

# Cargar trinkets.json
with open('trinkets.json', encoding='utf-8') as f:
    trinkets = json.load(f)

# Cargar plat.html
with open('plat.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Indexar trinkets del HTML por nombre
html_trinkets = {}
for li in soup.select('.alltrinkets li.textbox'):
    span = li.find('span')
    if not span:
        continue
    name_tag = span.find('p', class_='item-title')
    if not name_tag:
        continue
    name = name_tag.get_text(strip=True)
    # Descripción: todos los <p> sin clase
    description = [p.get_text(strip=True) for p in span.find_all('p', class_=False)]
    # Tags
    tags_tag = span.find('p', class_='tags')
    tags = tags_tag.get_text(strip=True) if tags_tag else ""
    # Unlock SOLO si hay <p class="r-unlock">
    unlock_tag = span.find('p', class_='r-unlock')
    unlock = unlock_tag.get_text(strip=True) if unlock_tag else ""
    html_trinkets[name] = {
        'description': description,
        'tags': tags,
        'unlock': unlock
    }

# Actualizar trinkets.json
for trinket in trinkets:
    name = trinket.get('name')
    if name in html_trinkets:
        trinket['description'] = html_trinkets[name]['description']
        trinket['tags'] = html_trinkets[name]['tags']
        # Solo añade unlock si existe y no está vacío
        if html_trinkets[name]['unlock']:
            trinket['unlock'] = html_trinkets[name]['unlock']
        elif 'unlock' in trinket:
            del trinket['unlock']

# Guardar resultado
with open('trinkets_actualizado.json', 'w', encoding='utf-8') as f:
    json.dump(trinkets, f, indent=2, ensure_ascii=False)

print("trinkets_actualizado.json generado con unlock solo para los que tienen r-unlock.")