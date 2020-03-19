import json

with open('norm.json', encoding='utf-8') as fh:
    data = json.load(fh)


with open("normYeni.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)