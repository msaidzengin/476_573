from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
import time
import json
import os


def dataFormat(chosen):
    """
    This method reads data.json and record them with turkish char letters. (utf-8)
    """
    try:
        with open('data.json', encoding='utf-8') as fh:
            data = json.load(fh)

        with open("data.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except:
        pass

def prepareData(chosenFile):
    print("a")


root = ThemedTk(theme = "black")
root.minsize(500,300)
root.title("NER GUI FOR TR")
root.iconbitmap('icon.ico')

subdirs = {}

root.include_training_data = {"1": BooleanVar(), "2": BooleanVar()}
root.include_training_data["1"].set(False)
root.include_training_data["2"].set(False)

root.classifier_methods = {"1": BooleanVar(), "2": BooleanVar()}
root.classifier_methods["1"].set(False)
root.classifier_methods["2"].set(False)

loadedDir = ""

def choose_file_out():
    cwd = os.getcwd()
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

    print(loadedDir)
    with open(loadedDir + "/out.json", 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=4)

    filename = ttk.Label(root.tab1, text = fname + " ✓", style = "S.TLabel").pack(pady = (10,0))

def choose_file():
    cwd = os.getcwd()
    filepath = filedialog.askopenfilename(initialdir = cwd , title = "Choose a file", filetype = (("json", "*.json"),))
    
    if filepath == '':
        return

    fname = filepath.split('/')[-1]
    dirname = fname.split('.')
    global loadedDir 
    loadedDir = dirname[0]

    print(loadedDir)

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

    if not os.path.exists(dirname[0]):
        os.makedirs(dirname[0])

    with open(dirname[0] + "/data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    filename = ttk.Label(root.tab1, text = fname + " ✓", style = "S.TLabel").pack(pady = (10,0))
    enter_file = ttk.Label(root.tab1, text = "Choose the output file (json)", style = "S.TLabel").pack(pady = (15,0))
    file_explorer = ttk.Button(root.tab1, text = "Choose a file", command=choose_file_out, style = "S.TButton").pack(pady = (15,0))



def preprocess():
    selection = list(Lb1.curselection())
    if len(selection) == 0:
        return

    chosenFile = subdirs[selection[0]]
    
    dataFormat(chosenFile)
    prepareData(chosenFile)
    
    
tabControl = ttk.Notebook(root)

root.tab1 = ttk.Frame(tabControl)
tabControl.add(root.tab1, text = "Load Data")

style = ttk.Style()
style.configure("S.TLabel", padding=(6,6), relief="flat", font = ('Verdana', 20))
style.configure("S.TCheckbutton", padding=(6,6), relief="flat", font = ('Verdana', 20), foreground = '#121926')
style.configure("S.TButton", padding=(6,6), relief="flat", font = ('Verdana', 20), background = '#121926')

enter_file = ttk.Label(root.tab1, text = "Choose the norm file (json)", style = "S.TLabel").pack(pady = (15,0))
file_explorer = ttk.Button(root.tab1, text = "Choose a file", command=choose_file, style = "S.TButton").pack(pady = (15,0))

root.tab2 = ttk.Frame(tabControl)
tabControl.add(root.tab2, text = "Preprocess")

cwd = os.getcwd()
"""
for dataName in next(os.walk('.'))[1]:
    root.training_algorithm[subcounter] = BooleanVar()
    root.training_algorithm[subcounter].set(False)
    root.transform_1 = ttk.Checkbutton(root.tab2, text=dataName, style = "S.TCheckbutton", var=root.training_algorithm[subcounter]).pack(pady = (55,0))
    subcounter += 1
"""
counter = 1
Lb1 = Listbox(root.tab2)
for dirName in next(os.walk('.'))[1]:
    Lb1.insert(counter, dirName)
    subdirs[counter - 1] = dirName
    counter += 1
Lb1.pack()
preprocessButton = ttk.Button(root.tab2, text = "Tamam", style = "S.TButton", command = preprocess).pack(pady = (35, 10))

root.tab3 = ttk.Frame(tabControl)
tabControl.add(root.tab3, text = "Train")

root.training_1 = ttk.Checkbutton(root.tab3, text = "Training Data 1", style = "S.TCheckbutton", var=root.include_training_data["1"],).pack(pady = (55,0))
root.training_2 = ttk.Checkbutton(root.tab3, text = "Training Data 2", style = "S.TCheckbutton", var=root.include_training_data["2"]).pack(pady = (10,0))

root.tab4 = ttk.Frame(tabControl)
tabControl.add(root.tab4, text = "Predict")

root.method_1 = ttk.Checkbutton(root.tab4, text = "Method 1", style = "S.TCheckbutton", var=root.classifier_methods["1"]).pack(pady = (30,0))
root.method_2 = ttk.Checkbutton(root.tab4, text = "Method 2", style = "S.TCheckbutton", var=root.classifier_methods["2"]).pack(pady = (10,0))

output = ttk.Button(root.tab4, text = "Sonuçlar", style = "S.TButton").pack(pady = (35,0))

tabControl.pack(expand = 1, fill = "both")


root.mainloop()
