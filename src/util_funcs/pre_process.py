import os
import pickle
from datetime import date

import numpy as np
import pandas as pd


def clean_data(df):
    """This function cleans and pre-processes the input DataFrame"""
    # Conversions into 'datetime' data type
    df['Year_Birth'] = pd.to_datetime(df['Year_Birth'], format='%Y')
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"])

    # get customer age
    # assuming analysis was conducted in 2014
    now = date.today()
    df['Age'] = now.year - df['Year_Birth'].dt.year

    # define the bin edges for age groups
    bins = [18, 28, 38, 48, 58, 65, np.inf]

    # define the labels for each age group
    labels = ['18-27', '28-37', '38-47', '48-57', '58-65', '65+']

    # create the age groups column
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    # Calculate the number of days since customer enrolled
    end_fiscal = pd.to_datetime(now)
    df['Onboard_Days'] = (end_fiscal - df['Dt_Customer']).dt.days

    # use overall spending
    spend_cols = [
        'MntWines',
        'MntFruits',
        'MntMeatProducts',
        'MntFishProducts',
        'MntSweetProducts',
        'MntGoldProds',
    ]
    df['Spending'] = df[spend_cols].sum(axis=1)

    # reduce categories in marital status
    marital_status = {
        'Divorced': 'Alone',
        'Single': 'Alone',
        'Married': 'In couple',
        'Together': 'In couple',
        'Absurd': 'Alone',
        'Widow': 'Alone',
        'YOLO': 'Alone',
    }
    df['Marital_Status'] = df['Marital_Status'].replace(marital_status)

    # reduce categories in education
    education_level = {
        'Basic': 'Undergraduate',
        '2n Cycle': 'Undergraduate',
        'Graduation': 'Postgraduate',
        'Master': 'Postgraduate',
        'PhD': 'Postgraduate',
    }
    df['Education'] = df['Education'].replace(education_level)

    # get the total count of children
    df['Children'] = df['Kidhome'] + df['Teenhome']

    # convert categorical features as categories
    categorical_ftrs = [
        'Education',
        'Marital_Status',
        'Age_Group',
        'Children',
        'AcceptedCmp3',
        'AcceptedCmp4',
        'AcceptedCmp5',
        'AcceptedCmp1',
        'AcceptedCmp2',
        'Complain',
    ]
    df[categorical_ftrs] = df[categorical_ftrs].astype('category')

    # drop redundant features
    redundant_features = [
        'Year_Birth',
        'Dt_Customer',
        'Age',
        'ID',
        'Kidhome',
        'Teenhome',
    ] + spend_cols
    df = df.drop(redundant_features, axis=1)

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
