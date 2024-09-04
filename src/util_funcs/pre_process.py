import os
import pickle
from datetime import date, datetime

import numpy as np
import pandas as pd

# fmt: off
# define the bin edges for age groups
bins = [18, 25, 35, 45, 55, 66, np.inf]

# define the labels for each age group
labels = ['Below 25', '25-34', '35-44', '45-54', '55-65', 'Above 65']

# spending columns
spend_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
              'MntSweetProducts', 'MntGoldProds']

# marital state re-coding
marital_status = { 'Divorced': 'Alone', 'Single': 'Alone', 'Married': 'In couple',
                  'Together': 'In couple', 'Absurd': 'Alone', 'Widow': 'Alone',
                  'YOLO': 'Alone'
                  }

# education level re-coding
education_level = {'Basic': 'Undergraduate', '2n Cycle': 'Undergraduate',
                   'Graduation': 'Postgraduate', 'Master': 'Postgraduate',
                   'PhD': 'Postgraduate'}

# categorical features
categorical_ftrs = ['Education', 'Marital_Status', 'Age_Group', 'Children', 'AcceptedCmp3',
                    'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1', 'AcceptedCmp2', 'Complain'
                    ]
# redundant features
redundant_features = ['Z_CostContact', 'Z_Revenue', 'Year_Birth', 'Dt_Customer', 'Age',
                          'ID', 'Kidhome', 'Teenhome', 'Response'] + spend_cols
# fmt: on


def clean_form_data(df):
    """This function cleans and pre-processes the input DataFrame"""
    # Conversions into 'datetime' data type
    df['Year_Birth'] = pd.to_datetime(df['Year_Birth'], format='%Y')
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"])

    # get customer age
    # assuming analysis was conducted in recent time
    now = date.today()
    df['Age'] = now.year - df['Year_Birth'].dt.year

    # create the age groups column
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    # number of days since customer enrolled converted to months
    end_fiscal = pd.to_datetime(now)
    df['Tenure'] = (end_fiscal - df['Dt_Customer']).dt.days
    df['Tenure'] = (df['Tenure'] / 30.44).round(1)

    # use overall spending
    df['Spending'] = df[spend_cols].sum(axis=1)

    # reduce categories in marital status
    df['Marital_Status'] = df['Marital_Status'].replace(marital_status)

    # reduce categories in education
    df['Education'] = df['Education'].replace(education_level)

    # get the total count of children
    df['Children'] = df['Kidhome'] + df['Teenhome']

    # convert categorical features as categories
    df[categorical_ftrs] = df[categorical_ftrs].astype('category')

    # drop redundant features
    for col in redundant_features:
        if col in df.columns:
            df = df.drop(col, axis=1)

    return df


# function to clean the file data
def clean_file_data(df):
    """This function cleans and pre-processes the input CSV DataFrame"""
    # Conversions into 'datetime' data type
    df['Year_Birth'] = pd.to_datetime(df['Year_Birth'], format='%Y')
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"])

    # get customer age
    # assuming analysis was conducted in 2014
    now = 2014
    df['Age'] = now - df['Year_Birth'].dt.year

    # create the age groups column
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    # number of days since customer enrolled converted to months
    end_fiscal = datetime(2014, 6, 30)
    df['Tenure'] = (end_fiscal - df['Dt_Customer']).dt.days
    df['Tenure'] = (df['Tenure'] / 30.44).round(1)

    # use overall spending
    df['Spending'] = df[spend_cols].sum(axis=1)

    # reduce categories in marital status
    df['Marital_Status'] = df['Marital_Status'].replace(marital_status)

    # reduce categories in education
    df['Education'] = df['Education'].replace(education_level)

    # get the total count of children
    df['Children'] = df['Kidhome'] + df['Teenhome']

    # fill missing values of income with the mean
    income_mean = df['Income'].mean()
    df['Income'] = df['Income'].fillna(income_mean)

    # turn categories into category dtype
    df[categorical_ftrs] = df[categorical_ftrs].astype('category')

    # drop redundant features
    for col in redundant_features:
        if col in df.columns:
            df = df.drop(col, axis=1)

    return df


def load_model(model_prefix="model_"):
    """
    Load the latest model from the specified directory with a given prefix.
    """

    # get absolute path of models directory
    model_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../..', 'models')
    )

    model_files = [
        f
        for f in os.listdir(model_dir)
        if f.startswith(model_prefix) and f.endswith('.pkl')
    ]

    if not model_files:
        raise FileNotFoundError(
            f"""No model files found starting with '{model_prefix}'
            in {model_dir} check if directory is labeled correctly"""
        )

    # Assuming the latest model is the last one alphabetically
    selected_model = model_files[-1]
    model_path = os.path.join(model_dir, selected_model)
    with open(model_path, 'rb') as f_in:
        model = pickle.load(f_in)
    return model
