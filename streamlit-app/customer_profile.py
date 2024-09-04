from datetime import date

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from dateutil.relativedelta import relativedelta

from util_funcs.pre_process import load_model, clean_form_data

styling_pred_output = """
<style>
    .pred-output {
        font-size: 20px;
        font-weight: bold;
        color: #4fc921;
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
</style>
"""

# inject the CSS into the app
st.markdown(styling_pred_output, unsafe_allow_html=True)


# load model and cache it
@st.cache_resource()
def get_model():
    """Caches the model loaded"""
    return load_model('dtc.pkl')


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
# fmt: off
with st.form(key='customer_form'):
    # expander for customer details
    with st.expander('Customer Details'):
        detail_1, detail_2, detail_3, detail_4 = st.columns(4)
        # create entry box with customer details (2 rows 4 columns)
        with detail_1:
            ID = st.number_input("ID", placeholder='20801', value=None, step=1)
            Year_Birth = st.number_input( "Year of Birth",
                                         min_value=max_age,
                                         max_value=min_age, value=None, placeholder=2006,
                                         help='Accepts age range of 18 to 120',)

        with detail_2:
            Education = st.selectbox( "Education",
                                     ["Basic", "2n Cycle", "Graduation", "Master", "PhD"],)
            marital_ = [ "Single", "Together", "Married", "Divorced", "Absurd", "Widow", "YOLO",]
            Marital_Status = st.selectbox("Marital Status", marital_)
        with detail_3:
            Income = st.number_input("Income", value=None, placeholder='0', step=1.0)
            Dt_Customer = st.date_input( "Date of Enrollment", min_value=consistent_gap,
                                        max_value=base_year,)
        with detail_4:
            Kidhome = st.number_input( r"\# of Kids (Tween)", step=1, value=None, placeholder='0',
                                      help='12 years and below', min_value=0,)
            Teenhome = st.number_input( r"\# of Teenagers", step=1, value=None, placeholder='0',
                                       min_value=0,)

    # expander of customer activity
    with st.expander('Customer Activity'):
        activity_1, activity_2, activity_3 = st.columns(3)

        with activity_1:
            NumDealsPurchases = st.number_input( "Number of Discounted Purchases", step=1,
                                                value=None, placeholder='0', min_value=0,
                                                max_value=20,)
            NumWebPurchases = st.number_input( "Number of Web Purchases", step=1, value=None,
                                              placeholder='0', min_value=0, max_value=35,)
            NumCatalogPurchases = st.number_input( "Number of Catalog Purchases", step=1,
                                                  value=None, placeholder='0', min_value=0,
                                                  max_value=35,)

        with activity_2:
            NumStorePurchases = st.number_input( "Number of Store Purchases", step=1,
                                                value=None, placeholder='0', min_value=0,
                                                max_value=20,)
            NumWebVisitsMonth = st.number_input( "Number of Web Visits in the Month", step=1,
                                                value=None, placeholder='0', min_value=0,
                                                max_value=25,
            )

        with activity_3:
            Recency = st.number_input( "Recency (Days since last purchase)", value=None,
                                      placeholder='0', min_value=0, max_value=110,
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
            MntMeatProducts = st.number_input( "Meat & Meat Products", value=None, placeholder='0',
                                              min_value=0, step=1)
            MntFishProducts = st.number_input( "Fish & Fish Products", value=None, placeholder='0',
                                              min_value=0, step=1,)

        with spending_3:
            MntSweetProducts = st.number_input( "Sweet Products", value=None, placeholder='0',
                                               min_value=0, step=1,)
            MntGoldProds = st.number_input( "Gold Products", value=None, placeholder='0',
                                           min_value=0, step=1,)

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
# fmt: on


# caching the preprocessing steps
@st.cache_data()
def process_data(all_fields):
    """Preprocess the input fields cache the step."""
    # check if all fields are filled
    if all(field is not None and field != "" for field in all_fields):
        # dictionary for non-binary entries
        # fmt: off
        non_binary_response_data = {
            'ID': ID, 'Year_Birth': Year_Birth, 'Education': Education,
            'Marital_Status': Marital_Status, 'Income': Income,
            'Dt_Customer': Dt_Customer, 'Kidhome': Kidhome,  'Teenhome': Teenhome,
            'NumDealsPurchases': NumDealsPurchases, 'NumWebPurchases': NumWebPurchases,
            'NumCatalogPurchases': NumCatalogPurchases,  'NumStorePurchases': NumStorePurchases,
            'NumWebVisitsMonth': NumWebVisitsMonth, 'Recency': Recency,  'MntWines': MntWines,
            'MntFruits': MntFruits,  'MntMeatProducts': MntMeatProducts,
            'MntFishProducts': MntFishProducts, 'MntSweetProducts': MntSweetProducts,
            'MntGoldProds': MntGoldProds,
        }

        # convert yes/no response to 0/1
        binary_fields = ['Complain','AcceptedCmp1','AcceptedCmp2','AcceptedCmp3','AcceptedCmp4',
                         'AcceptedCmp5',]
        # fmt: on
        binary_response_data = {
            field: 1 if all_fields[binary_fields.index(field)] == 'Yes' else 0
            for field in binary_fields
        }
        # join both dictionaries
        non_binary_response_data.update(binary_response_data)

        # convert to DataFrame
        df = pd.DataFrame([non_binary_response_data])

        return df
    st.error("You might have forgotten something 😊.")
    return None


# customer profile from the processed and cleaned data
# fmt: off
def customer_profile(processed_df, cleaned_df):
    """Create a customer profile based on the processed and clean data."""

    processed_fields = [ID, Income, Marital_Status, Education]
    processed_df = pd.DataFrame([processed_fields],
                                columns=['ID', 'Income', 'Marital Status', 'Education Level'])
    clean_fields = ['Spending', 'Children', 'Tenure', 'Age_Group', 'Recency']

    profile_df = pd.concat([processed_df, cleaned_df[clean_fields]], axis=1)
    st.markdown("""
             To better understand why, here is a quick summary of his/her profile that
             you can compare to the dashboard below for those who accepted the offer:
             """)
    st.write(profile_df)
# fmt: on


# load dashboard and cache it
# pylint: disable=line-too-long
@st.cache_data
def load_dashboard():
    components.html(
        """
        <div class='tableauPlaceholder' id='viz1725413884334' style='position: relative'><noscript><a href='#'><img alt='Dashboard 3 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;C2&#47;C2B96T5CS&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;C2B96T5CS' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;C2&#47;C2B96T5CS&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1725413884334');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='1520px';vizElement.style.height='1007px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
        """,
        height=900,
        scrolling=True,
    )


# pylint: enable=line-too-long


if submitted:
    # fmt: off
    input_fields = [
        ID, Year_Birth, Education, Marital_Status, Income, Dt_Customer, Kidhome, Teenhome,
        NumDealsPurchases, NumWebPurchases, NumCatalogPurchases, NumStorePurchases,
        NumWebVisitsMonth, Recency, Complain, MntWines, MntFruits, MntMeatProducts,
        MntFishProducts, MntSweetProducts, MntGoldProds, AcceptedCmp1, AcceptedCmp2, AcceptedCmp3,
        AcceptedCmp4, AcceptedCmp5,
    ]
    # fmt: on
    df_processed = process_data(input_fields)
    if df_processed is not None:
        # load the model
        model = get_model()

        # cleaned data
        df_clean = clean_form_data(df_processed)

        # give prediction
        prediction = model.predict(df_clean.to_dict('records'))[0]
        if prediction == 1:
            message = f"Customer {ID} is likely to accept the offer"
        else:
            message = f"Customer {ID} is likely to reject the offer"

        # Display the customer's category
        st.markdown(
            f"<div class='pred-output'>{message}</div>", unsafe_allow_html=True
        )

        # get customer profile
        customer_profile(processed_df=df_processed, cleaned_df=df_clean)

        # tableau dashboard
        with st.expander("Show Dashboard"):
            load_dashboard()
