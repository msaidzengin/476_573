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
        outWords = out['text'].split(' ')
        if len(outWords) == 1:
            train_data.append(outWords[0] + " S-" + out['category'])
        else:
            for i in range(len(outWords)):
                if i == 0:
                    train_data.append(outWords[i] + " B-" + out['category'])
                elif i == len(outWords) - 1:
                    train_data.append(outWords[i] + " E-" + out['category'])
                else:
                    train_data.append(outWords[i] + " I-" + out['category'])

        text = text.replace(out['text'], '')
        
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    text = text.split(' ')
    for word in text:
        if word != '':
            train_data.append(word + " O")

    train_data.append("")
    print(idd)

train = {
    "data" : train_data
}

with open("train.txt", "w", encoding='utf8') as text_file:
    for d in train_data:
        text_file.write(d + "\n")
text_file.close()

print('finished')