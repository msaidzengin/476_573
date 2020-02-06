from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import time


root = Tk()
root.minsize(300,200);
root.title("Turkish NER with GUI")
root.iconbitmap('icon.ico')

input_training_data = [0,0]
training_algorithm = [0,0]
include_training_data = [0,0]
classifier_methods = [0,0]

def choose_file():
    file_name = filedialog.askopenfilename(initialdir = "/" , title = "Choose a file", filetype = (("json", "*.json"),))
    label = Label(root, text = "").pack()

def write():
    print(training_algorithm[0])
    
    
tabControl = ttk.Notebook(root)

root.tab1 = ttk.Frame(tabControl)
tabControl.add(root.tab1, text = "Eğitim Verisi Gir")
 
root.tab2 = ttk.Frame(tabControl)
tabControl.add(root.tab2, text = "Eğitim Verisi Temizleme Algoritması Seç")

root.tab3 = ttk.Frame(tabControl)
tabControl.add(root.tab3, text = "Örnek Eğitim Verisi Ekle")

root.tab4 = ttk.Frame(tabControl)
tabControl.add(root.tab4, text = "Transform Algorithms")

tabControl.pack(expand = 1, fill = "both")


enter_file = Label(root.tab1, text = "Choose a file to process (json) :").pack()
file_explorer = Button(root.tab1, text = "Choose a file", command=choose_file).pack()

transform_1 = ttk.Checkbutton(root.tab2, text="Algorithm 1", state="Unchecked", variable=training_algorithm[0], onvalue=1, offvalue=0, command=write ).pack()
transform_2 = ttk.Checkbutton(root.tab2, text="Algorithm 2", state="Unchecked", variable=training_algorithm[1], onvalue=1, offvalue=0).pack()

training_1 = ttk.Checkbutton(root.tab3, text = "Training Data 1", state="Unchecked", variable=include_training_data[0], onvalue=1, offvalue=0).pack()
training_2 = ttk.Checkbutton(root.tab3, text = "Training Data 2", state="Unchecked", variable=include_training_data[1], onvalue=1, offvalue=0).pack()

method_1 = ttk.Checkbutton(root.tab4, text = "Method 1", state="Unchecked", variable=classifier_methods[0], onvalue=1, offvalue=0).pack()
method_2 = ttk.Checkbutton(root.tab4, text = "Method 2", state="Unchecked", variable=classifier_methods[1], onvalue=1, offvalue=0).pack()

output = Button(root.tab4, text = "Sonuçlar").pack(side=RIGHT)



root.mainloop()

