# proj-food_in_the_hood

## Contents

- App Folder 
    - manage.py - script for creating dash dahsboard visualization
    - decision_tree.py - script for analyzing data using a decision tree classification model
    - install.sh - shell script for creating the virtual environment
    - requirements.txt - text file of required libraries to install in virtual environment

- Data Folder
    - get_data_from_atlas.py - script for getting data from Chicago Health Atlas
    - food_data.csv - main file data file for dashboard visualizations and decision tree analysis
    - visual.ipynb - jupyter notebook for data visualizations
    - merge_and_visual_csv.ipynb - jupyter notebook for data visualizations
    - several other csv files, jupyter notebooks for data visualizations

    - Crime Folder
        - get_data_from_portal.py - script for getting data from Chicago Data Portal
        - several csv files related to crime data

## Running The Software

Code to run from the command line

1. `bash install.sh`
2. `source env/bin/activate`
3. `python3 decision_tree.py & python3 manage.py`

## Examples of Interacting with the Software

- The result from running decision_tree.py is a dictionary where the keys are the following strings: ‘all variables’, 'adult_fruit_and_vegetable_servings_rate', 'adult_soda_consumption_rate', 'low_food_access', 'poverty_rate', and 'population'). The value associated with ‘all variables’ is the rate at which a model using all attribute variables was successful in predicting the crime rate. That is, how well did a model using all attributes in food_data.csv do at predicting the target class? A model with all variables predicted the crime rate correctly about 55% of the time. The remaining keys are associated with values that show how well a model did at predicting the crime rate excluding that variable from building the model. For example, the “poverty_rate” key is associated with a value of about 41%, meaning a model built without the poverty rate attribute predicted the crime rate correctly 41% of the time.
- The result from running manage.py creates an interactive dashboard. You can interact with the dashboard to choose a variable to explore in more detail from the left sidebar drop down menu. Below the dropdown menu, a more complete description of the selected variable will appear. For example, 
![2022-03-12](https://user-images.githubusercontent.com/89871328/158085158-16b0c583-0934-493f-9d10-0b0c8bbf6b71.jpg)
