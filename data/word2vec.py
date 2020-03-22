import json
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

with open('normYeni.json', encoding='utf-8') as fh:
    data = json.load(fh)

with open("sentences.txt", "w", encoding='utf8') as text_file:
    for d in data['data']:
        text_file.write(d['text'] + "\n")
text_file.close()
print("sentences.txt kaydedildi")

model = Word2Vec(LineSentence("sentences.txt"), size=400, window=5, min_count=1, workers=multiprocessing.cpu_count())
model.wv.save_word2vec_format("wordEmbeddings.txt")
print("bitti")