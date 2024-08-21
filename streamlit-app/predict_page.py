import os
from datetime import date

import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta

from util_funcs.pre_process import clean_data, load_model

# load css file
css_path = os.path.abspath('styles.css')
with open(css_path, encoding='utf8') as f:
    css = f.read()

# injecting css into the app
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# load model and cache it
st.cache_resource()


def get_model():
    """Caches the model loaded"""
    return load_model('rfc.pkl')


# user can be between 18 to 120 years
base_year = date.today()
max_age = base_year.year - 120
min_age = base_year.year - 18


# consistency in date of enrollment since the data was collected
# between 2012 to 2014 but we want to mimic that to the current year
# the start and end date are values retrieved from the data
start_date = date(2012, 6, 1)
end_date = date(2014, 6, 30)
difference = relativedelta(end_date, start_date)
consistent_gap = base_year - difference

# main form with the sub forms in expanders
with st.form(key='customer_form'):
    # expander for customer details
    with st.expander('Customer Details'):
        detail_1, detail_2, detail_3, detail_4 = st.columns(4)
        # create entry box with customer details (2 rows 4 columns)
        with detail_1:
            ID = st.number_input("ID", placeholder='20801', value=None, step=1)
            Year_Birth = st.number_input(
                "Year of Birth",
                min_value=max_age,
                max_value=min_age,
                value=None,
                placeholder=2006,
                help='Accepts age range of 18 to 120',
            )

        with detail_2:
            Education = st.selectbox(
                "Education",
                ["Basic", "2n Cycle", "Graduation", "Master", "PhD"],
            )
            marital_ = [
                "Single",
                "Together",
                "Married",
                "Divorced",
                "Absurd",
                "Widow",
                "YOLO",
            ]
            Marital_Status = st.selectbox("Marital Status", marital_)
        with detail_3:
            Income = st.number_input(
                "Income", value=None, placeholder='0', step=1.0
            )
            Dt_Customer = st.date_input(
                "Date of Enrollment",
                min_value=consistent_gap,
                max_value=base_year,
            )
        with detail_4:
            Kidhome = st.number_input(
                r"\# of Kids (Tween)",
                step=1,
                value=None,
                placeholder='0',
                help='12 years and below',
                min_value=0,
            )
            Teenhome = st.number_input(
                r"\# of Teenagers",
                step=1,
                value=None,
                placeholder='0',
                min_value=0,
            )

    # expander of customer activity
    with st.expander('Customer Activity'):
        activity_1, activity_2, activity_3 = st.columns(3)

        with activity_1:
            NumDealsPurchases = st.number_input(
                "Number of Discounted Purchases",
                step=1,
                value=None,
                placeholder='0',
                min_value=0,
                max_value=20,
            )
            NumWebPurchases = st.number_input(
                "Number of Web Purchases",
                step=1,
                value=None,
                placeholder='0',
                min_value=0,
                max_value=35,
            )
            NumCatalogPurchases = st.number_input(
                "Number of Catalog Purchases",
                step=1,
                value=None,
                placeholder='0',
                min_value=0,
                max_value=35,
            )

        with activity_2:
            NumStorePurchases = st.number_input(
                "Number of Store Purchases",
                step=1,
                value=None,
                placeholder='0',
                min_value=0,
                max_value=20,
            )
            NumWebVisitsMonth = st.number_input(
                "Number of Web Visits in the Month",
                step=1,
                value=None,
                placeholder='0',
                min_value=0,
                max_value=25,
            )

        with activity_3:
            Recency = st.number_input(
                "Recency (Days since last purchase)",
                value=None,
                placeholder='0',
                min_value=0,
                max_value=110,
            )
            Complain = st.radio("Complained in the Past 2 Years", ["No", "Yes"])

    # expander for customer spending
    with st.expander('Customer Spending in the Past 2 Years'):
        spending_1, spending_2, spending_3 = st.columns(3)

        with spending_1:
            MntWines = st.number_input(
                "Wines", value=None, placeholder='0', min_value=0, step=1
            )
            MntFruits = st.number_input(
                "Fruits", value=None, placeholder='0', min_value=0, step=1
            )

        with spending_2:
            MntMeatProducts = st.number_input(
                "Meat & Meat Products",
                value=None,
                placeholder='0',
                min_value=0,
                step=1,
            )
            MntFishProducts = st.number_input(
                "Fish & Fish Products",
                value=None,
                placeholder='0',
                min_value=0,
                step=1,
            )

        with spending_3:
            MntSweetProducts = st.number_input(
                "Sweet Products",
                value=None,
                placeholder='0',
                min_value=0,
                step=1,
            )
            MntGoldProds = st.number_input(
                "Gold Products",
                value=None,
                placeholder='0',
                min_value=0,
                step=1,
            )

    # expander for customer campaign participation
    with st.expander('Previous Campaign Responses'):
        campaign_1, campaign_2, campaign_3 = st.columns(3)

        with campaign_1:
            AcceptedCmp1 = st.radio(
                "Accepted Offer in 1st Campaign", ["No", "Yes"]
            )
            AcceptedCmp3 = st.radio(
                "Accepted Offer in 3rd Campaign", ["No", "Yes"]
            )

        with campaign_2:
            AcceptedCmp2 = st.radio(
                "Accepted Offer in 2nd Campaign", ["No", "Yes"]
            )
            AcceptedCmp4 = st.radio(
                "Accepted Offer in 4th Campaign", ["No", "Yes"]
            )

        with campaign_3:
            AcceptedCmp5 = st.radio(
                "Accepted Offer in 5th Campaign", ["No", "Yes"]
            )

    # submit button for all forms
    submitted = st.form_submit_button(
        'Submit', type='primary', use_container_width=True
    )


# caching the preprocessing steps
@st.cache_data()
def preprocess_data(all_fields):
    """Preprocess the input fields cache the step."""
    # check if all fields are filled
    if all(field is not None and field != "" for field in all_fields):
        # dictionary for non-binary entries
        non_binary_response_data = {
            'ID': ID,
            'Year_Birth': Year_Birth,
            'Education': Education,
            'Marital_Status': Marital_Status,
            'Income': Income,
            'Dt_Customer': Dt_Customer,
            'Kidhome': Kidhome,
            'Teenhome': Teenhome,
            'NumDealsPurchases': NumDealsPurchases,
            'NumWebPurchases': NumWebPurchases,
            'NumCatalogPurchases': NumCatalogPurchases,
            'NumStorePurchases': NumStorePurchases,
            'NumWebVisitsMonth': NumWebVisitsMonth,
            'Recency': Recency,
            'MntWines': MntWines,
            'MntFruits': MntFruits,
            'MntMeatProducts': MntMeatProducts,
            'MntFishProducts': MntFishProducts,
            'MntSweetProducts': MntSweetProducts,
            'MntGoldProds': MntGoldProds,
        }

        # convert yes/no response to 0/1
        binary_fields = [
            'Complain',
            'AcceptedCmp1',
            'AcceptedCmp2',
            'AcceptedCmp3',
            'AcceptedCmp4',
            'AcceptedCmp5',
        ]
        binary_response_data = {
            field: 1 if all_fields[binary_fields.index(field)] == 'Yes' else 0
            for field in binary_fields
        }
        # join both dictionaries
        non_binary_response_data.update(binary_response_data)

        # convert to DataFrame
        df = pd.DataFrame([non_binary_response_data])

        # preprocess the data
        df_clean = clean_data(df)

        return df_clean
    st.error("You might have forgotten something 😊.")
    return None


if submitted:
    input_fields = [
        ID,
        Year_Birth,
        Education,
        Marital_Status,
        Income,
        Dt_Customer,
        Kidhome,
        Teenhome,
        NumDealsPurchases,
        NumWebPurchases,
        NumCatalogPurchases,
        NumStorePurchases,
        NumWebVisitsMonth,
        Recency,
        Complain,
        MntWines,
        MntFruits,
        MntMeatProducts,
        MntFishProducts,
        MntSweetProducts,
        MntGoldProds,
        AcceptedCmp1,
        AcceptedCmp2,
        AcceptedCmp3,
        AcceptedCmp4,
        AcceptedCmp5,
    ]

    df_preprocessed = preprocess_data(input_fields)
    if df_preprocessed is not None:
        # load the model
        model = get_model()

        # give prediction
        prediction = model.predict(df_preprocessed.to_dict('records'))[0]
        if prediction == 1:
            message = f"<span class='positive'>Customer {ID} is likely to accept the offer</span>"
        else:
            message = f"<span class='negative'>Customer {ID} is likely to reject the offer</span>"

        # Display the styled message
        st.markdown(message, unsafe_allow_html=True)
