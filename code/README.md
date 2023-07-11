# README

# Simulated data
'gen_static_data_script.py' generates the simulated data we used in this work.

# Researcher Support Platform
'Researcher Support Platform-v2.py' presents the python code of a simple UI as the basis for our solution to receive information from researchers on their trial designs and produce an estimate of the retention rate and provide some suggestions on how to improve retention rate. The objective is to extend it to have a dynamic suggestion system which requires more granualr information. 

The GUI is currently working based on the simulated data to provide retention estimate and suggestions to improve retention (please refer to 'Counterfactual+recommend.ipynb' under notrbook).

For running the GUI, please run:

    python Researcher_Support_Platform.py

A page will be represented to enter the design information. Please see below an example:

![alt text](http://url/to/step1.png)

Then you can press an retention estimate to get and estimate of your retention rate:



# notebook

This folder include the code for recommender system.

'Counterfactual_recommend.ipynb' includes the retention estimate and recommendation system. model-lr and model_weights.pth are learnt on simulated data and saved to be used in the platform.

# Joint Research Platform
(2) 'jointplatform.html' is a web interface showing the basis for a joint research platform on mental health research for (i) participants to reseagister their interest, (ii) researchers to get support and be matched to participants and (iii) both to be able interact. The final solution aims to provide a ML model to match participants to researchers with the main aim of long term retention. 

'html code - researcher platform' includes that html codes for web interface.

# Participant Support Platform
Participantplatform.html is a web interface showing the basis for a participant support system which enables participants to receive training information, updates on the trial progress and the option to provide feedback. Access to this platform will password protected in the final solution. 
'prg1.jpg', 'prg2.jpg', and 'trial.jpg' are used in this interface. 

'html code - participant platform' include that html codes for web interface.

# arxiv
'ret_estimate-v1.ipynb' provides some early preprocessing and GP implementation to estimate retentio. This version is trained on information we extracted from a few online trials. 'retention_estimation-v2.ipynb' was trained on an initial simulated data but then we decided to use a Counterfactual recommender and a linear model based on the final simulated data.
