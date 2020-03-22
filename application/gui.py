from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog
import time

root = ThemedTk(theme = "black")
root.minsize(500,300)
root.title("NER GUI FOR TR")
root.iconbitmap('icon.ico')

root.input_training_data = {"1": BooleanVar(), "2": BooleanVar()}
root.input_training_data["1"].set(False)
root.input_training_data["2"].set(False)

root.training_algorithm = {"1": BooleanVar(), "2": BooleanVar()}
root.training_algorithm["1"].set(False)
root.training_algorithm["2"].set(False)

root.include_training_data = {"1": BooleanVar(), "2": BooleanVar()}
root.include_training_data["1"].set(False)
root.include_training_data["2"].set(False)

root.classifier_methods = {"1": BooleanVar(), "2": BooleanVar()}
root.classifier_methods["1"].set(False)
root.classifier_methods["2"].set(False)

def choose_file():
    file_name = filedialog.askopenfilename(initialdir = "/" , title = "Choose a file", filetype = (("json", "*.json"),))
    label = ttk.Label(root, text = "").pack()
    return file_name
    
    
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

root.transform_1 = ttk.Checkbutton(root.tab2, text="Algorithm 1", style = "S.TCheckbutton", var=root.training_algorithm["1"]).pack(pady = (55,0))
root.transform_2 = ttk.Checkbutton(root.tab2, text="Algorithm 2", style = "S.TCheckbutton", var=root.training_algorithm["2"]).pack(pady = (10,0))

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
