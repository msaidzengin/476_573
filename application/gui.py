from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import time


root = Tk()
root.minsize(600,400);
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
    label = Label(root, text = "").pack()
    return file_name
    

    
    
tabControl = ttk.Notebook(root)

root.tab1 = ttk.Frame(tabControl)
tabControl.add(root.tab1, text = "Load Data")

enter_file = Label(root.tab1, text = "Choose a file to process (json) :").pack()
file_explorer = Button(root.tab1, text = "Choose a file", command=choose_file).pack()

root.tab2 = ttk.Frame(tabControl)
tabControl.add(root.tab2, text = "Preprocess")

root.transform_1 = ttk.Checkbutton(root.tab2, text="Algorithm 1", var=root.training_algorithm["1"]).pack()
root.transform_2 = ttk.Checkbutton(root.tab2, text="Algorithm 2", var=root.training_algorithm["2"]).pack()

root.tab3 = ttk.Frame(tabControl)
tabControl.add(root.tab3, text = "Train")

root.training_1 = ttk.Checkbutton(root.tab3, text = "Training Data 1", var=root.include_training_data["1"]).pack()
root.training_2 = ttk.Checkbutton(root.tab3, text = "Training Data 2", var=root.include_training_data["2"]).pack()

root.tab4 = ttk.Frame(tabControl)
tabControl.add(root.tab4, text = "Predict")

root.method_1 = ttk.Checkbutton(root.tab4, text = "Method 1", var=root.classifier_methods["1"]).pack()
vmethod_2 = ttk.Checkbutton(root.tab4, text = "Method 2", var=root.classifier_methods["2"]).pack()

output = Button(root.tab4, text = "Sonuçlar").pack(side=RIGHT)

tabControl.pack(expand = 1, fill = "both")




root.mainloop()



