import json
from bs4 import BeautifulSoup

# Cargar cards.json
with open('cards.json', encoding='utf-8') as f:
    cards = json.load(f)

# Cargar plat.html
with open('plat.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Indexar cartas del HTML por nombre
html_cards = {}
for li in soup.select('.allcards li.textbox'):
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
    html_cards[name] = {
        'description': description,
        'tags': tags,
        'unlock': unlock
    }

# Actualizar cards.json
for card in cards:
    name = card.get('name')
    if name in html_cards:
        card['description'] = html_cards[name]['description']
        card['tags'] = html_cards[name]['tags']
        # Solo añade unlock si existe y no está vacío
        if html_cards[name]['unlock']:
            card['unlock'] = html_cards[name]['unlock']
        elif 'unlock' in card:
            del card['unlock']

# Guardar resultado
with open('cards_actualizado.json', 'w', encoding='utf-8') as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print("cards_actualizado.json generado con unlock solo para los que tienen r-unlock.")