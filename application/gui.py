from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
import string
import time
import json
import os
import json
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

def wordEmbedding(chosenFile):

    with open('NCRFpp/data/' + chosenFile + '/data.json', encoding='utf-8') as fh:
        data = json.load(fh)

    with open('NCRFpp/data/' + chosenFile + '/sentences.txt', "w", encoding='utf8') as text_file:
        for d in data['data']:
            text_file.write(d['text'] + "\n")
    text_file.close()

    model = Word2Vec(LineSentence('NCRFpp/data/' + chosenFile + "/sentences.txt"), size=400, window=5, min_count=1, workers=multiprocessing.cpu_count())
    model.wv.save_word2vec_format('NCRFpp/data/' + chosenFile + "/sample.word.emb")

def prepareData(chosenFile):

    with open('NCRFpp/data/' + chosenFile + '/data.json', encoding='utf-8') as fh:
        data = json.load(fh)

    with open('NCRFpp/data/' + chosenFile + '/out.json', encoding='utf-8') as fh:
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

    
    total = len(train_data)
    train = int(total * 0.7)
    test = int(total * 0.15)
    dev = int(total * 0.15)

    with open('NCRFpp/data/' + chosenFile + "/train.bmes", "w", encoding='utf8') as fl:
        for line in train_data[ : train]:
            fl.write(line + "\n")
    fl.close()

    with open('NCRFpp/data/' + chosenFile + "/test.bmes", "w", encoding='utf8') as fl:
        for line in train_data[ train : train + test ]:
            fl.write(line + "\n")
    fl.close()

    with open('NCRFpp/data/' + chosenFile + "/dev.bmes", "w", encoding='utf8') as fl:
        for line in train_data[ train + test : ]:
            fl.write(line + "\n")
    fl.close()

    with open('NCRFpp/data/' + chosenFile + "/raw.bmes", "w", encoding='utf8') as fl:
        for line in train_data[ train + test : ]:
            fl.write(line + "\n")
    fl.close()


root = ThemedTk(theme = "black")
root.minsize(500,300)
root.title("NER GUI FOR TR")
root.iconbitmap('icon.ico')

subdirs = {}
subdirs2 = {}

root.include_training_data = {"1": BooleanVar(), "2": BooleanVar()}
root.include_training_data["1"].set(False)
root.include_training_data["2"].set(False)

root.classifier_methods = {"1": BooleanVar(), "2": BooleanVar()}
root.classifier_methods["1"].set(False)
root.classifier_methods["2"].set(False)

loadedDir = ""
counter = 1
counter2 = 1
cwd = os.getcwd()

def choose_file_out():

    filepath = filedialog.askopenfilename(initialdir = cwd , title = "Choose a file", filetype = (("json", "*.json"),))
    
    if filepath == '':
        return

    fname = filepath.split('/')[-1]
    dirn = fname.split('.')

    if dirn[-1] != 'json':
        errorr = ttk.Label(root.tab1, text = "wrong format", style = "S.TLabel").pack(pady = (10,0))
        return

    with open(filepath, encoding='utf-8') as fh:
        out = json.load(fh)

    try:
        temp = out['data'][0]['text']
        idd = out['data'][0]['id']
    except:
        errorr = ttk.Label(root.tab1, text = "wrong json format", style = "S.TLabel").pack(pady = (10,0))
        return

    with open('NCRFpp/data/' + loadedDir + "/out.json", 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=4)

    filename = ttk.Label(root.tab1, text = fname + " ✓", style = "S.TLabel").pack(pady = (10,0))

    dirs = list(subdirs.values())
    if loadedDir not in dirs:
        Lb1.insert(counter, loadedDir)
        subdirs[counter - 1] = loadedDir


def choose_file():

    filepath = filedialog.askopenfilename(initialdir = cwd , title = "Choose a file", filetype = (("json", "*.json"),))
    
    if filepath == '':
        return

    fname = filepath.split('/')[-1]
    dirname = fname.split('.')
    global loadedDir 
    loadedDir = dirname[0]

    if dirname[-1] != 'json':
        errorr = ttk.Label(root.tab1, text = "wrong format", style = "S.TLabel").pack(pady = (10,0))
        return

    with open(filepath, encoding='utf-8') as fh:
        data = json.load(fh)

    try:
        temp = data['data'][0]['text']
    except:
        errorr = ttk.Label(root.tab1, text = "wrong json format", style = "S.TLabel").pack(pady = (10,0))
        return

    if not os.path.exists('NCRFpp/data/' + dirname[0]):
        os.makedirs('NCRFpp/data/' + dirname[0])

    with open('NCRFpp/data/' + dirname[0] + "/data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    filename = ttk.Label(root.tab1, text = fname + " ✓", style = "S.TLabel").pack(pady = (10,0))
    enter_file = ttk.Label(root.tab1, text = "Choose the output file (json)", style = "S.TLabel").pack(pady = (15,0))
    file_explorer = ttk.Button(root.tab1, text = "Choose a file", command=choose_file_out, style = "S.TButton").pack(pady = (15,0))



def preprocess():
    selection = list(Lb1.curselection())
    if len(selection) == 0:
        return

    chosenFile = subdirs[selection[0]]
    
    wordEmbedding(chosenFile)
    prepareData(chosenFile)

    filename = ttk.Label(root.tab2, text = "Done ✓", style = "S.TLabel").pack(pady = (10,0))
    
    dirs = list(subdirs2.values())
    if chosenFile not in dirs:
        Lb2.insert(counter2, chosenFile)
        subdirs2[counter2 - 1] = chosenFile

def train():
    selection = list(Lb2.curselection())
    if len(selection) == 0:
        return
    
    chosenFile = subdirs[selection[0]]
    if os.getcwd().split('\\')[-1] != "NCRFpp":
        os.chdir("NCRFpp")

    newconfig = ""
    lineCounter = 0
    trainConfig = open("demo.train.config", "r")
    for line in trainConfig:
        if "train_dir" in line:
            newconfig += "train_dir=data/" + chosenFile + "/train.bmes\n"
        elif "dev_dir" in line:
            newconfig += "dev_dir=data/" + chosenFile + "/dev.bmes\n"
        elif "test_dir" in line:
            newconfig += "test_dir=data/" + chosenFile + "/test.bmes\n"
        elif "model_dir" in line and lineCounter < 8:
            newconfig += "model_dir=data/" + chosenFile + "/lstmcrf\n"
        elif "word_emb_dir" in line:
            newconfig += "word_emb_dir=data/" + chosenFile + "/sample.word.emb\n"
        else:
            newconfig += line
        lineCounter += 1
    trainConfig.close()
    newConf = open("demo.train.config", "w")
    newConf.write(newconfig)
    newConf.close
    time.sleep(1)
    os.system('python main.py --config demo.train.config')
    
    
tabControl = ttk.Notebook(root)

root.tab1 = ttk.Frame(tabControl)
tabControl.add(root.tab1, text = "Load Data")

root.tab2 = ttk.Frame(tabControl)
tabControl.add(root.tab2, text = "Preprocess")

root.tab3 = ttk.Frame(tabControl)
tabControl.add(root.tab3, text = "Train")

root.tab4 = ttk.Frame(tabControl)
tabControl.add(root.tab4, text = "Predict")

style = ttk.Style()
style.configure("S.TLabel", padding=(6,6), relief="flat", font = ('Verdana', 20))
style.configure("S.TCheckbutton", padding=(6,6), relief="flat", font = ('Verdana', 20), foreground = '#121926')
style.configure("S.TButton", padding=(6,6), relief="flat", font = ('Verdana', 20), background = '#121926')

enter_file = ttk.Label(root.tab1, text = "Choose the norm file (json)", style = "S.TLabel").pack(pady = (15,0))
file_explorer = ttk.Button(root.tab1, text = "Choose a file", command=choose_file, style = "S.TButton").pack(pady = (15,0))

Lb1 = Listbox(root.tab2)
Lb2 = Listbox(root.tab3)

if not os.path.exists('NCRFpp/data'):
        os.makedirs('NCRFpp/data')

for dirName in next(os.walk(cwd + '/NCRFpp/data'))[1]:

    Lb1.insert(counter, dirName)
    subdirs[counter - 1] = dirName

    Lb2.insert(counter2, dirName)
    subdirs2[counter2 - 1] = dirName

    counter += 1
    counter2 += 1

Lb1.pack()
Lb2.pack()
preprocessButton = ttk.Button(root.tab2, text = "Tamam", style = "S.TButton", command = preprocess).pack(pady = (35, 10))
preprocessButton = ttk.Button(root.tab3, text = "Tamam", style = "S.TButton", command = train).pack(pady = (35, 10))

root.method_1 = ttk.Checkbutton(root.tab4, text = "Method 1", style = "S.TCheckbutton", var=root.classifier_methods["1"]).pack(pady = (30,0))
root.method_2 = ttk.Checkbutton(root.tab4, text = "Method 2", style = "S.TCheckbutton", var=root.classifier_methods["2"]).pack(pady = (10,0))

output = ttk.Button(root.tab4, text = "Sonuçlar", style = "S.TButton").pack(pady = (35,0))

tabControl.pack(expand = 1, fill = "both")


root.mainloop()
