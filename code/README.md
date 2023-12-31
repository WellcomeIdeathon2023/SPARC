# README
We aim to address the challenges of participant retention in long-term mental health clinical trials by providing researchers with estimation and guidance, enabling seamless communication between researchers and participants, and empowering participants with information and resources to stay engaged in the trials. At this stage, we have laid the foundation for our final solution. We divided our solution to three platforms; researcher support platform, joint research platform, and participant platform.

# Data Simulation
'gen_static_data_script.py' is a parser written in Python that can parse a json file to generate simulated data.  Only three parameters can be specified to run this python file: config_path, save_path, and seed. The config_path is the path to the json file that contains the parameters for the simulation. The save_path is the path to the csv file that the simulated data will be saved to. The seed is the random seed for the simulation.

``` 
python gen_static_data_script.py --config_path config.json --save_path output.csv --seed 0
```

Please find instructions for the json config file [here](https://github.com/WellcomeIdeathon2023/SPARC/blob/main/data/README.md).

# Researcher Support Platform
'Researcher Support Platform-v2.py' presents the python code of a simple UI as the basis for our solution to receive information from researchers on their trial designs and produce an estimate of the retention rate and provide some suggestions on how to improve retention rate. The objective is to extend it to have a dynamic suggestion system which requires more granualr information. 

The GUI is currently working based on the simulated data to provide retention estimate and suggestions to improve retention (please refer to 'Counterfactual_recommend.ipynb' under notrbook).

model-lr and model_weights.pth are the saved models based on simulated data used in the GUI. 

For running the GUI, please run:

    python Researcher_Support_Platform.py

A page will be represented to enter the design information. Please see below an example:

<p align="center">
<img src="step1.png" alt="Alt Text" width="40%">
</p>

Then you can press an Retention Rate to get and estimate of your retention rate. If you are looking for recommnedations to increse the retention you can you Recoomendations and enter your desired value.

<p align="center">
<img src="step2.png" alt="Alt Text" width="25%">
</p>

# notebook

This folder include the code for recommender system.

'Counterfactual_recommend.ipynb' includes the retention estimate and recommendation system. model-lr and model_weights.pth are learnt on simulated data and saved to be used in the platform.

# Joint Research Platform
'joint_platform.html' is a web interface showing the basis for a joint research platform on mental health research for (i) participants to reseagister their interest, (ii) researchers to get support and be matched to participants and (iii) both to be able interact. The final solution aims to provide a ML model to match participants to researchers with the main aim of long term retention. 

'joint_platform.rtf' includes that html codes for web interface.

# Participant Support Platform
Participantplatform.html is a web interface showing the basis for a participant support system which enables participants to receive training information, updates on the trial progress and the option to provide feedback. Access to this platform will password protected in the final solution. 
'prg1.jpg', 'prg2.jpg', and 'trial.jpg' are used in this interface. 

'html code - participant platform' include that html codes for web interface.

# arxiv
'ret_estimate-v1.ipynb' provides some early preprocessing and GP implementation to estimate retentio. This version is trained on information we extracted from a few online trials. 'retention_estimation.ipynb' was trained on an initial simulated data but then we decided to use a Counterfactual recommender and a linear model based on the final simulated data.
