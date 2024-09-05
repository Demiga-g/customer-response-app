import streamlit as st

st.markdown(
    """
    <h1 style="color:#4fc921">iFood's Marketing Campaign App</h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
### About the App!

This dummy application was developed to assist iFood's marketing team in improving the performance of
their marketing campaigns.
Faced with challenges in profit growth over the next three years, the company's marketing department
was tasked with spending its budget more wisely.
The solution was to adopt a more data-driven approach by building a predictive model to support
direct marketing initiatives.

### Model Performance:

- The models were able to correctly predict over 75 percent of clients who would
accept an offer.
- Additionally, the model achieved an overall accuracy of over 87 percent.

### Benefits:

- The app allows for a single variable entry to make predictions or a batch output where a user can
upload a csv file with the data.
- For the single variable entry, users have the advantage of comparing the model's predictions with
the Tableau dashboard to assess the reasonableness of the response and make informed decisions.

*Use the sidebar to navigate through the app and explore the features.*


### Downsides:

- The data used is from 2014, this implies that the dates used here have been simulated to match the
dates when the data was collected.
Otherwise, there would be disparity when calculating customers' age and tenure period.
- There are are also restriction to values that can be inserted to some measures to disallow
for outliers.

### Disclaimer

- The model may not provide an exact prediction for each client, as it is a statistical model.
- Users may need to interpret the model's output to make informed decisions, which may involve
additional data analysis or consultation with domain experts.
- The model may not be as accurate as a human expert in marketing, so the predictions should be
used as a starting point for further analysis and decision-making.
"""
)
