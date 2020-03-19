import json
import string

with open('normYeni.json', encoding='utf-8') as fh:
    data = json.load(fh)


with open('output.json', encoding='utf-8') as fh:
    output = json.load(fh)

train_data = []

for i in data['data']:
    idd = i['id']
    text = i['text']

    outs = []

    for j in output['data']:
        if j['id'] == idd:
            outs.append(j)

    for out in outs:
        train_data.append(out['text'] + " " + out['category'])
        text = text.replace(out['text'], '')
        
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    text = text.split(' ')
    for word in text:
        if word != '':
            train_data.append(word + " 0")

    train_data.append("")
    print(idd)

train = {
    "data" : train_data
}

with open("train.json", 'w', encoding='utf-8') as f:
    json.dump(train, f, ensure_ascii=False, indent=4)
