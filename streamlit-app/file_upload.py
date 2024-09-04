import pandas as pd
import streamlit as st

from util_funcs.pre_process import load_model, clean_file_data


# load model and cache it
@st.cache_resource
def get_model():
    """Caches the model loaded"""
    return load_model('xgb.pkl')


# file upload function
def file_upload_form():
    upload_file = st.file_uploader("Choose a CSV file", type="csv")
    process_file = st.button('Process File')
    return upload_file, process_file


# process the csv file
def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df_clean = clean_file_data(df)
        model = get_model()
        predictions = model.predict(df_clean.to_dict('records'))
        df['Prediction'] = predictions
        return df
    return None


# generate output
uploaded_csv, processed_file = file_upload_form()
if processed_file and uploaded_csv is not None:
    df_with_predictions = process_uploaded_file(uploaded_csv)
    if df_with_predictions is not None:
        st.subheader("Prediction Results")

        # get those who would accept offer and their IDs
        filtered_df = df_with_predictions[
            df_with_predictions['Prediction'] == 1
        ]
        count_client = filtered_df.shape[0]
        ids_ = filtered_df['ID'].astype(str).tolist()
        ids_string = ", ".join(ids_)
        st.success(
            f"""
                   There are {count_client} customers who are likely to accept the offer.
                   These are customers with the following IDs: {ids_string}."""
        )

        # display the results in a table
        st.write(df_with_predictions)

        # download link for the results
        csv = df_with_predictions.to_csv(index=False)
        st.download_button(
            label="Download predictions as CSV",
            data=csv,
            file_name="predictions.csv",
            mime="text/csv",
        )
    else:
        st.error(
            "Error processing the file. Please check the format and try again."
        )
