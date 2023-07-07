# README

# Simulated data
'gen_static_data_script.py' generates the simulated data we used in this work.

# Researcher Support Platform
(1) 'Researcher Support Platform-v2.py' presents the python code of a simple UI as the basis for our solution to receive information from researchers on trial designs and produce an estimate of the retention rate and provide some suggestions. The objective is to extend it to have a dynamic suggestion system which requires more granualr information. Current system generate information based on simulated data. 

The GUI (1) is currently working based on the simulated data to provide retention estimate and suggestions to improve retention (please refer to 'Counterfactual+recommend.ipynb').

'retention_estimation-v1.ipynb' provides some early preprocessing and GP implementation to estimate retentio. This version is trained on information we extracted from a few online trials. 'retention_estimation-v2.ipynb' was trained on an initial simulated data but then we decided to use a Counterfactual recommender and a linear model based on the final simulated data.

'Counterfactual+recommend.ipynb' includes the retention estimate and recommendation system.

# Joint Research Platform
(2) 'jointplatform.html' is a web interface showing the basis for a joint research platform on mental health research for (i) participants to reseagister their interest, (ii) researchers to get support and be matched to participants and (iii) both to be able interact. The final solution aims to provide a ML model to match participants to researchers with the main aim of long term retention. 

# Participant Support Platform
(3) Participantplatform.html is a web interface showing the basis for a participant support system which enables participants to receive training information, updates on the trial progress and the option to provide feedback. Access to this platform will password protected in the final solution. 
'prg1.jpg', 'prg2.jpg', and 'trial.jpg' are used in this interface. 

'html code - researcher platform' and 'html code - oarticipant platform' include that html codes for web interfaces in (2) and (3).


