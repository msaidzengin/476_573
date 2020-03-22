from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
import time
import json
import os

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

def choose_file():
    cwd = os.getcwd()
    filepath = filedialog.askopenfilename(initialdir = cwd , title = "Choose a file", filetype = (("json", "*.json"),))
    
    if filepath == '':
        return

    fname = filepath.split('/')[-1]
    dirname = fname.split('.')

    if dirname[-1] != 'json':
        errorr = ttk.Label(root.tab1, text = "wrong format", style = "S.TLabel").pack(pady = (40,0))
        return

    with open(filepath, encoding='utf-8') as fh:
        data = json.load(fh)

    try:
        temp = data['data'][0]['text']
    except:
        errorr = ttk.Label(root.tab1, text = "wrong json format", style = "S.TLabel").pack(pady = (40,0))
        return

    if not os.path.exists(dirname[0]):
        os.makedirs(dirname[0])

    with open(dirname[0] + "/data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    filename = ttk.Label(root.tab1, text = fname + " ✓", style = "S.TLabel").pack(pady = (40,0))

def preprocess():
    selection = list(Lb1.curselection())
    if len(selection) == 0:
        return

    choosenData = subdirs[selection[0]]
    
    
    
tabControl = ttk.Notebook(root)

root.tab1 = ttk.Frame(tabControl)
tabControl.add(root.tab1, text = "Load Data")

style = ttk.Style()
style.configure("S.TLabel", padding=(6,6), relief="flat", font = ('Verdana', 20))
style.configure("S.TCheckbutton", padding=(6,6), relief="flat", font = ('Verdana', 20), foreground = '#121926')
style.configure("S.TButton", padding=(6,6), relief="flat", font = ('Verdana', 20), background = '#121926')

enter_file = ttk.Label(root.tab1, text = "Choose a file to process (json) :", style = "S.TLabel").pack(pady = (40,0))
file_explorer = ttk.Button(root.tab1, text = "Choose a file", command=choose_file, style = "S.TButton").pack(pady = (20,0))

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
