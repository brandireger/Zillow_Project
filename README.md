# Zillow Project

## Purpose
This project aims to predict the values of single unit properties using property data during the "hot months" (in terms of real estate demand) of May and June in 2017.

The customer is the Zillow data science team.

## Deliverables
1. Presentation: [Link] (https://docs.google.com/presentation/d/1AD6-7jxczQzKK85wtslh7gobS2jAsDsABuZel2Rg3Tk/edit?usp=sharing)
    - Must include what state and county the properties are located in
    - Must include distribution of tax rates for each county
    - Summarizes findings about the drivers of property values
2. Github Repository: [Link](https://github.com/brandireger/Zillow_Project)
    - Readme (this file)
    - Final Jupyter notebook walking through the pipeline
    - .py files with all functions necessary to reproduce the model

## Pipeline

# Planning
- New Hypotheses:
    - $H_a$: Engineered features will improve predictions
- Failed to reject Hypotheses:
    - $H_a$: Value is predicted best by all features in dataset
- Rejected Hypotheses:
    - $H_0$: Value is not predictable by any features in the dataset
    - $H_a$: Value is predicted best by number of beds
    - $H_a$: Value is predicted best by number of baths
    - $H_a$: Value is predicted best by sq feet

- Predictor Features (independent):
    - First model: sq feet, number of bedrooms, number of bathrooms

- Predicted Feature (dependent): 'taxvaluedollarcnt' aka value

- Feature Engineering Ideas: 
    - Combine bathroom and bedrooms into bath_bed
    - Calculate age of home
    - Make is_extra column for features like pool, fireplace, hot tub, etc


# Acquire Data
- Goal: a prepared dataframe
    - Create a file called acquire.py with all necessary functions to generate this dataframe from SQL

# Data Preparation
- Goal: a prepared dataframe
    - address missing & null values, data integrity issues, etc.
        - Bathrooms: 40 properties with 0 baths
        - Bedrooms: 42 properties with 0 beds
        - Square_feet: 24 null properties
        - fips: added new columns: county and state based on this column
        - Tax_Amount: 1 null value
        * Decided to drop all null and 0 values
        * Decided to drop fips column since it was replaced by County and State columns
    - plot distributions of variables
        - identify outliers
        - decide how/if to scale features
        - find errors or invalid data
    - data dictionary
        1. parcelid = identifier of each property
        2. bathrooms = number of bathrooms. Used field named 'bathroomcnt' instead of 'calculatedbathnbr' or 'fullbathcnt' because the other two fields included nulls, and were essentially the same. Dropped rows with 0 bathrooms, to ensure I was only looking at single residence homes.
        3. bedrooms = number of bedrooms. No other fields seemed to contain this info. Dropped rows with 0 bedrooms, to ensure I was only looking at single residence homes.
        4. square_feet = size of home. Used field 'calculatedfinishedsquarefeet' because it was identical to 'finishedsquarefeet12', the other square feet fields were mostly nulls.
        5. Value = value of property. Used field named 'taxvaluedollarcnt' because it was specified in the project specifications.
        6. tax_amount = amunt of taxes charged. Used field named 'taxamount'.
        7. county = name of county the property is from. This field came from the fips identifier in the original databse. The website I obtained the names of counties from: [link] (https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697)
        8. state = name of state. This field came from the fips identifier in the original databse. The website I obtained the names of counties from: [link] (https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697)
        9. tax_rate = calculated field created by dividing the value of the property by the tax_amount.

# Split & Scale
- Goal: two prepared dataframes (train & test) and scaled data
    - Create a file called split_scale.py with all necessary functions to generate this dataframe

# Data Exploration
- Goal: Address questions generated during planning and preparation phases
    - Run at least one t-test and one correlation test
        - Two sample t-test: compares means of two subgroups
        * Used 
    - Visualize all combinations of variables
    - Questions to answer:
        - What independent variables are correlated with the dependent? (good)
        - Which independent variables are correlated with other independent variables? (not good)
    - Summarize takeaways and conclusions

# Feature Selection
- Goal: a dataframe with the features to be used to build the model
    - Are there new features that can be generated from existing features? (only to be done if there is time)
    - Use feature selection techniques
    - Create a file called feature_selection.py with all necessary functions to generate this dataframe

# Modeling & Evaluation
- Goal: develop a regression model that performs better than a baseline
    - Create baseline model
    - Show how model outperforms baseline
    - Notebook has extra algorithms and hyperparameters tried, with evaluation code and results
    - Evaluate by:
        - plot residuals
        - compute evaluation metrics (SSE, MSE, RMSE)
        - compare to baseline
        - plot y(actual) by y(predicted)
    - Create a file called model.py with all necessary functions to fit, predict and evaluate the model