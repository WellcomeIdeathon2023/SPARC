import tkinter as tk
from tkinter import messagebox

def help_action():
    if not validate_values():
        return

    pop_up_window = tk.Toplevel(window)
    pop_up_window.title("Help")
    pop_up_window.geometry("200x100")

    retention_label = tk.Label(pop_up_window, text="retention")
    retention_label.pack(pady=20)

def retention_action():
    if not validate_values():
        return

    pop_up_window = tk.Toplevel(window)
    pop_up_window.title("Retention")
    pop_up_window.geometry("200x100")

    retention_label = tk.Label(pop_up_window, text="retention rate is: ")
    retention_label.pack(pady=20)

def recommendations_action():
    if not validate_values():
        return

    pop_up_window = tk.Toplevel(window)
    pop_up_window.title("Recommendations")
    pop_up_window.geometry("200x100")

    retention_label = tk.Label(pop_up_window, text="Please see the following recommnedations: ")
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
    age_range_gt_65 = entries["Age range >65 %"].get()
    white_ethnicity = entries["White ethnicity %"].get()
    other_ethnicity = entries["Other ethnicity %"].get()

    if age_range_18_65.isdigit() and age_range_gt_65.isdigit() and white_ethnicity.isdigit() and other_ethnicity.isdigit():
        age_range_18_65 = int(age_range_18_65)
        age_range_gt_65 = int(age_range_gt_65)
        white_ethnicity = int(white_ethnicity)
        other_ethnicity = int(other_ethnicity)

        age_sum = age_range_18_65 + age_range_gt_65
        ethnicity_sum = white_ethnicity + other_ethnicity

        if age_sum != 100:
            messagebox.showerror("Invalid Input", "The sum of 'Age range (18-65) %' and 'Age range >65 %' should be equal to 100.")
            return False

        if ethnicity_sum != 100:
            messagebox.showerror("Invalid Input", "The sum of 'White ethnicity %' and 'Other ethnicity %' should be equal to 100.")
            return False

    return True


window = tk.Tk()

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
    "Age range (18-65) %": None,
    "Age range >65 %": None,
    "Male %": None,
    "White ethnicity %": None,
    "Other ethnicity %": None,
    "Medication": None,
    "Follow up considered": None,
    "Use of wearables": None,
    "Use of mobile app": None,
    "Training sessions": None,
    "Interviews needed": None,
    "Questionnaire completed": None,
    "Feedback to users provided": None,
    "Use of technology to support": None,
    "Prior treatment history considered": None,
    "Co-morbidities considered": None,
    "Income level": None,
    "Treatment type": None,
    "Biosample collection (e.g. blood, tissue)": None,
    "Is randomized": None,
    "Insurance": None,
    "Multi-site": None,
    "Adverse event considered": None,
    "Support sessions": None,
    "Self-management": None
}

entries = {}

for name, _ in name_entry.items():
    label = tk.Label(window_frame, text=name + ":")
    label.pack()

    if name in ["Number of Participants", "Study Duration - weeks"]:
        var = tk.StringVar()
        entry = tk.Entry(window_frame, validate="key")
        entry.configure(validatecommand=(entry.register(validate_positive_integer), "%P"))
        entry.pack()

        entries[name] = entry
    elif name in ["Age range (18-65) %", "Age range >65 %", "Male %", "White ethnicity %","Other ethnicity %"]:
        var = tk.StringVar()
        entry = tk.Entry(window_frame, validate="key")
        entry.configure(validatecommand=(entry.register(validate_percentage), "%P"))
        entry.pack()

        entries[name] = entry
    elif name == "Income level":
        var = tk.StringVar()
        entry = tk.OptionMenu(window_frame, var, "Low", "Median", "High")
        entry.pack()

        entries[name] = var
    elif name in ["Follow up considered", "Use of wearables", "Use of mobile app",
                "Training sessions", "Interviews needed", "Questionnaire completed",
                "Feedback to users provided", "Use of technology to support",
                "Prior treatment history considered", "Co-morbidities considered",
                "Biosample collection (e.g. blood, tissue)", "Is randomized",
                "Insurance", "Multi-site", "Adverse event considered",
                "Support sessions", "Self-management"]:
        var = tk.StringVar()
        entry = tk.OptionMenu(window_frame, var, "Yes", "No")
        entry.pack()

        entries[name] = var
    else:
        entry = tk.Entry(window_frame)
        entry.pack()

        name_entry[name] = entry
        entries[name] = entry

help_button = tk.Button(window_frame, text="Help", command=help_action)
help_button.pack()

retention_button = tk.Button(window_frame, text="Retention Rate", command=retention_action)
retention_button.pack()

recommendations_button = tk.Button(window_frame, text="Recommendations", command=recommendations_action)
recommendations_button.pack()

result_label = tk.Label(window_frame)
result_label.pack()

canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

window.mainloop()
