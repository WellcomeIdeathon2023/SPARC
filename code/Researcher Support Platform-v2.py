import tkinter as tk
from tkinter import messagebox
import pickle
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset
import tqdm

#models for recommendation estimation
class Linear(nn.Module):
    def __init__(self, weights,bias):
        super(Linear, self).__init__()
        self.weights = weights
        self.bias = bias        
    
    def forward(self, x):
        y = torch.matmul(x,self.weights)+self.bias
        return y
    
def query_recommendation(query_x,target_y,model,query_features,max_iters=200):
    
    query_y = model(query_x)
    feature_ids = [0, 1, 2, 3, 4]
    
    loss_fn = torch.nn.MSELoss(reduction='mean')
    
    cx,cy = conterfactual_infer(query_x,target_y,feature_ids, model, loss_fn, max_iters)
    
    # diff = torch.abs(query_x-cx).reshape(-1)
    
    # cf = []
    # print(diff)
    # for i in range(len(diff)):
    #     if diff[i]>0.01:
    #         cf.append(query_features[i])
    # cf.append(query_features[diff[feature_ids].argmax()])
    # cx = cx.detach().numpy().reshape(-1)
    # cx = cx[diff.argmax()]
    features = ['n_participant', 'duration', 'age>65', 'male', 'ethnicity_white',
       'adverse_event_considered_no', 'adverse_event_considered_yes',
       'biosamples_collected_no', 'biosamples_collected_yes',
       'co_mobidities_considered_no', 'co_mobidities_considered_yes',
       'feedback_provided_no', 'feedback_provided_yes',
       'follow_up_considered_no', 'follow_up_considered_yes',
       'interviews_needed_no', 'interviews_needed_yes', 'medication_5ARI',
       'medication_Antidepressant', 'medication_Escitalopram',
       'medication_Testosterone', 'medication_citalopram',
       'medication_venlafaxine', 'mutli_site_no', 'mutli_site_yes',
       'prioir_treatment_history_considered_no',
       'prioir_treatment_history_considered_yes', 'questionare_completed_no',
       'questionare_completed_yes', 'randomised_no', 'randomised_yes',
       'support_sessions_no', 'support_sessions_yes',
       'treatment_type_behavioural', 'treatment_type_medication',
       'treatment_type_observational', 'treatment_type_rTMS',
       'use_mobile_app_no', 'use_mobile_app_yes', 'use_technology_no',
       'use_technology_yes', 'use_wearables_no', 'use_wearables_yes']

    diff = torch.abs(query_x-cx).reshape(-1)
    cf = features[diff>0]
    cx = cx[:,diff>0]
    
    return cx.detach().numpy().reshape(-1),cy.detach().numpy(),cf

def conterfactual_infer(query_x,target_y,feature_ids, model, loss_fn, max_iters):
    model.eval()
    tqdm_range = tqdm.tqdm(range(max_iters))
    cx = torch.clone(query_x)
    cx.requires_grad = True
    cf_optimizer = torch.optim.Adam([cx], lr=0.01)
    mask = torch.ones_like(query_x).type(torch.bool)
    mask[:,feature_ids] = False
    for it in tqdm_range:
        cy = model(cx)
        loss = loss_fn(cy,target_y)#loss_fn(query_x,cx,cy,target_y,feature_ids)
        loss.backward()
        cx.grad[mask]=0.
        cf_optimizer.step()
        cf_optimizer.zero_grad()

        if (it+1)%10 == 0:    
            tqdm_range.write('iter: {}, loss: {}'.format(it+1, loss.detach()))
    return cx, model(cx)

#help section
def help_action():
    if not validate_values():
        return

    pop_up_window = tk.Toplevel(window)
    pop_up_window.title("Help")
    pop_up_window.geometry("500x200")

    retention_label = tk.Label(pop_up_window, text="Please see the following information: \n Duration considered for up to 10 years. \n For medication currently the following options are considered: \n Testosterone', '5ARI', 'citalopram', 'Antidepressant', 'Escitalopram', 'venlafaxine'. \n and for treetment_types, the following options: \n 'behavioural', 'observational', 'rTMS', 'medication'. \n Please press 'Retention' to get an estimate of your retention rate and \n 'Recommendations'  to get design support.")
    retention_label.pack(pady=20)

# estimating retention
def retention_action(flag=True):
    values = []
    # estimate retention based on saved model
    continuous = ["Number of Participants", "Study Duration - weeks","Age range 18-65 %", "Male %", "White ethnicity %"]
    medication_list = ['Testosterone', '5ARI', 'citalopram', 'Antidepressant',
       'Escitalopram', 'venlafaxine'] #a small list to be updated for final solution
    
    m = pd.get_dummies(medication_list)
    
    treetment_types = ['behavioural', 'observational', 'rTMS', 'medication']
    t = pd.get_dummies(treetment_types)
    
    binary = ['No','Yes']
    b = pd.get_dummies(binary)
    
    if flag:
        pop_up_window = tk.Toplevel(window)
        pop_up_window.title("Retention")
        pop_up_window.geometry("200x100")
    model = pickle.load(open('model-lr', 'rb'))
    
    for name, _ in name_entry.items():
        x = entries[name].get()
        if x == '' and name in continuous:
            values.append(0)
        elif name in continuous:
            x = int(x)
            if name == "Number of Participants":
                x = x/99999 # normalise to maximum possible participants
            elif name == "Study Duration - weeks":
                x = x/500
            else:
                x = x/100
            values.append(x)
        else: 
            if name == 'Medication':
                if x =='':
                    x = [0,0,0,0,0,0]
                else:
                    x = m[x].values    
            elif name == 'Treatment type':
                if x =='':
                    x = [0,0,0,0]
                else:
                    x = t[x].values
            else:

                if x =='':
                    x = [0,0]
                else:
                    x = b[x].values
            for elm in x:
                values.append(elm)
    
    if sum(values) == 0 and flag:
        retention_label = tk.Label(pop_up_window, text='No value provided!')
        retention_label.pack(pady=20)
    else:
        prd = model.predict(np.array(values).reshape(1, -1))
        if flag:
            retention_label = tk.Label(pop_up_window, text="Predicted retention rate is: "+ str(round(prd[0]*100,2)))
            retention_label.pack(pady=20)
    
    return values, prd

#providing desired value to get recommendations
def submit_action():
    pop_up_window = tk.Toplevel(window)
    pop_up_window.title("Recommendations to consider")
    pop_up_window.geometry("400x100")
    
    if entries['rec'].get() =='':
        suggestion_label = tk.Label(pop_up_window, text="You need to enter your desired rate: ")
        suggestion_label.grid(row=1, column=0)
    else:
        query_features = ["n_participant","Duration of the study","age>65","male","ethnicity_white"]
        target_y = int(entries['rec'].get())/100
        lrg = pickle.load(open('model-lr', 'rb'))
        model = Linear(weights=torch.Tensor(lrg.coef_),bias=torch.ones(1)*lrg.intercept_)
        model.load_state_dict(torch.load('model_weights.pth'))
        values, pred = retention_action(False)
        query_x = torch.Tensor(np.array(values).astype(np.float32))
        query_x = query_x.reshape(1,-1)
        cx, cy, cf = query_recommendation(query_x,target_y=torch.ones(query_x.shape[0])*target_y,query_features=query_features,model=model)
        qstr = " ".join([cf[i]+" --> "+str(cx[i])+";" for i in range(len(cf))])
        suggestion_label = tk.Label(pop_up_window, text=f"The recommendations is to change:"+ qstr+'\n The new retention rate would be '+str(cy[0].round(3)))
        suggestion_label.grid(row=1, column=0)
   # suggestion_label = tk.Label(pop_up_window, text="You need to change: ")
  #  suggestion_label.grid(row=1, column=0)


def recommendations_action():
    pop_up_window = tk.Toplevel(window)
    pop_up_window.title("Recommendations")
    pop_up_window.geometry("250x100")
    
    values, pred = retention_action(False)
    if sum(values) == 0:
        sug_label = tk.Label(pop_up_window, text='No value provided for design! \n please enter your design values first!')
        sug_label.grid(row=1, column=0)
    else:
        sug_label = tk.Label(pop_up_window, text="The predicted retention rate is "+ str(round(pred[0]*100,2)) +". \nPlease enter your desired rate (%): ")
        sug_label.grid(row=1, column=0)
        var = tk.StringVar()
        entry = tk.Entry(pop_up_window, validate="key", textvariable = var)
        entry.configure(validatecommand=(entry.register(validate_positive_integer), "%P"))
        entry.grid(row=2, column=0)
        entries['rec'] = var
        submit_button = tk.Button(pop_up_window, text="Submit", command=submit_action)
        submit_button.grid(row=3, column=0)    
    
    
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

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
    return True


window = tk.Tk()
window.title("Researcher Platform")
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
    "Adverse event considered": None,
    "Biosample collection (e.g. blood, tissue)": None,
    "Co-morbidities considered": None,
    "Feedback to users provided": None,
    "Follow up considered": None,
    "Interviews needed": None,
    "Medication": None,
    "Prior treatment history considered": None,
    "Multi-site": None,
    "Questionnaire completed": None,
    "Is randomized": None,
    "Support sessions": None,
    "Treatment type": None,
    "Use of mobile app": None,
    "Use of technology to support": None,
    "Use of wearables": None,
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
