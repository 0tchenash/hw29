import csv
import json
with open('data/ad.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    for row in rows:
        if row['is_published'] == 'TRUE':
            row['is_published'] = True
        else:
            row['is_published'] = False 
with open('data/ad.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=4)

with open('data/category.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
with open('data/category.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=4)

with open('data/location.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
with open('data/location.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=4)

with open('data/user.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
with open('data/user.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=4)