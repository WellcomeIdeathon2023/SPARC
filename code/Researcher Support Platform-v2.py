import tkinter as tk
from tkinter import messagebox
import pickle
import numpy as np
import pandas as pd

def help_action():
    if not validate_values():
        return

    pop_up_window = tk.Toplevel(window)
    pop_up_window.title("Help")
    pop_up_window.geometry("200x100")

    retention_label = tk.Label(pop_up_window, text="retention")
    retention_label.pack(pady=20)

def retention_action():
    values = []
    medication_list = ['Testosterone', '5ARI', 'citalopram', 'Antidepressant',
       'Escitalopram', 'venlafaxine'] #a small list to be updated for final solution
    
    m = pd.get_dummies(medication_list)
    
    treetment_types = ['behavioural', 'observational', 'rTMS', 'medication']
    t = pd.get_dummies(treetment_types)
    
    pop_up_window = tk.Toplevel(window)
    pop_up_window.title("Retention")
    pop_up_window.geometry("200x100")
    model = pickle.load(open('model1', 'rb'))
    
    for name, _ in name_entry.items():
        x = entries[name].get()
        if x == '' and name !='Medication' and name != "Treatment type":
            values.append(0)
        elif x == 'No':
            x = 0
            values.append(x)
        elif x == 'Yes':
            x = 1
            values.append(x)
        elif name !='Medication' and name != "Treatment type":
            x = int(x)
            if name == "Number of Participants":
                x = x/99972 # normalise to maximum possible participants
            elif name == "Study Duration - weeks":
                x = x/84
            else:
                x = x/100
            values.append(x)
        else: 
            if name == 'Medication':
                if x =='':
                    x = [0,0,0,0,0,0]
                else:
                    x = m[x].values    
            else:
                if x =='':
                    x = [0,0,0,0]
                else:
                    x = t[x].values
            for elm in x:
                values.append(elm)
    prd = model.predict(np.array(values).reshape(1, -1))
    
    print(values)
    if sum(values) == 0:
        retention_label = tk.Label(pop_up_window, text='No value provided!')
    else:
        retention_label = tk.Label(pop_up_window, text="retention rate is: "+ str(round(prd[0]*100,2)))
    retention_label.pack(pady=20)

def recommendations_action():
    if not validate_values():
        return

    pop_up_window = tk.Toplevel(window)
    pop_up_window.title("Recommendations")
    pop_up_window.geometry("200x100")

    retention_label = tk.Label(pop_up_window, text="Please see the following recommendations: ")
    retention_label.pack(pady=20)


def validate_positive_integer(input_value):
    if input_value.isdigit():
        return True
    elif input_value == "":
        return True
    else:
        return False

def validate_percentage(input_value):
    if input_value.isdigit():
        value = int(input_value)
        if 0 <= value <= 100:
            return True
    elif input_value == "":
        return True
    return False

def validate_values():
    age_range_18_65 = entries["Age range (18-65) %"].get()
    white_ethnicity = entries["White ethnicity %"].get()

    if age_range_18_65.isdigit() and white_ethnicity.isdigit():
        age_range_18_65 = int(age_range_18_65)

        white_ethnicity = int(white_ethnicity)

    return True


window = tk.Tk()

window.geometry("550x700")

canvas = tk.Canvas(window)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

window_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=window_frame, anchor="nw")

name_entry = {
    "Number of Participants": None,
    "Study Duration - weeks": None,
    "Age range 18-65 %": None,
    "Male %": None,
    "White ethnicity %": None,
    "Use of technology to support": None,
    "Follow up considered": None,
    "Use of wearables": None,
    "Use of mobile app": None,
    "Interviews needed": None,
    "Questionnaire completed": None,
    "Feedback to users provided": None,
    "Prior treatment history considered": None,
    "Co-morbidities considered": None,
    "Biosample collection (e.g. blood, tissue)": None,
    "Is randomized": None,
    "Multi-site": None,
    "Adverse event considered": None,
    "Support sessions": None,
    "Medication": None,
    "Treatment type": None,
}

entries = {}
i=0
for name, _ in name_entry.items():
    label = tk.Label(window_frame, text=name + ":")
    label.grid(row=i, column=0)

    if name in ["Number of Participants", "Study Duration - weeks"]:
        var = tk.StringVar()
        entry = tk.Entry(window_frame, validate="key", textvariable = var)
        entry.configure(validatecommand=(entry.register(validate_positive_integer), "%P"))
   #     entry.pack()
        entry.grid(row=i, column=1)

        entries[name] = entry
    elif name in ["Age range 18-65 %", "Male %", "White ethnicity %"]:
        var = tk.StringVar()
        entry = tk.Entry(window_frame, validate="key", textvariable = var)
        entry.configure(validatecommand=(entry.register(validate_percentage), "%P"))
#        entry.pack()
        entry.grid(row=i, column=1)
        entries[name] = entry

        entries[name] = var
    elif name in ["Follow up considered", "Use of wearables", "Use of mobile app",
                "Training sessions", "Interviews needed", "Questionnaire completed",
                "Feedback to users provided", "Use of technology to support",
                "Prior treatment history considered", "Co-morbidities considered",
                "Biosample collection (e.g. blood, tissue)", "Is randomized",
                "Multi-site", "Adverse event considered",
                "Support sessions", "Self-management"]:
        var = tk.StringVar()
        entry = tk.OptionMenu(window_frame, var, "Yes", "No")
 #       entry.pack()
        entry.grid(row=i, column=1)
        entries[name] = var
    else:
        print(name)
        var = tk.StringVar()
        entry = tk.Entry(window_frame,textvariable = var)
  #      entry.pack()

        entries[name] = var
        entry.grid(row=i, column=1)
    i=i+1


retention_button = tk.Button(window_frame, text="Retention Rate", command=retention_action)
retention_button.grid(row=i, column=1)
i=i+1

recommendations_button = tk.Button(window_frame, text="Recommendations", command=recommendations_action)
recommendations_button.grid(row=i, column=1)
i=i+1

result_label = tk.Label(window_frame)
#result_label.pack()

help_button = tk.Button(window_frame, text="Help", command=help_action)
help_button.grid(row=i, column=1)
i=i+1

canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

window.mainloop()
