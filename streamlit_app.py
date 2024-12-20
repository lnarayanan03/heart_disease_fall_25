import json
import streamlit as st
import requests
import pandas as pd  # Import pandas for creating a DataFrame

st.title('Heart Disease Prediction')

# Initialize user options dictionary
user_options = {}

# Load slider fields from JSON
streamlit_options = json.load(open("streamlit_options.json"))

# Mapping of field names to full descriptions
field_name_mapping = {
    'age': 'Age',
    'sex': 'Sex (Male/Female)',
    'cp': 'Chest Pain Type',
    'trestbps': 'Resting Blood Pressure',
    'chol': 'Serum Cholesterol (mg/dl)',
    'fbs': 'Fasting Blood Sugar > 120 mg/dl (Yes/No)',
    'restecg': 'Resting Electrocardiographic Results',
    'thalach': 'Maximum Heart Rate Achieved',
    'exang': 'Exercise Induced Angina (Yes/No)',
    'oldpeak': 'ST Depression Induced by Exercise',
    'slope': 'Slope of the Peak Exercise ST Segment',
    'ca': 'Number of Major Vessels Colored by Fluoroscopy',
    'thal': 'Thalassemia'
}

# Custom display options for specific fields
custom_options = {
    "sex": {"Male": 1, "Female": 0},
    "fbs": {"True (Yes)": 1, "False (No)": 0},
    "exang": {"Yes": 1, "No": 0}
}

for field_name, range_values in streamlit_options["slider_fields"].items():
    min_val, max_val = range_values
    # If the field has custom display options
    if field_name in custom_options:
        display_labels = list(custom_options[field_name].keys())
        selected_label = st.sidebar.radio(field_name_mapping[field_name], options=display_labels)
        user_options[field_name] = custom_options[field_name][selected_label]  # Get value from label
    elif min_val == 0 and max_val == 1:
        # Use radio for binary fields without custom options
        user_options[field_name] = st.sidebar.radio(
            field_name_mapping[field_name], options=[0, 1], index=0
        )
    else:
        # Use slider for other ranges
        current_value = round((min_val + max_val) / 2)
        user_options[field_name] = st.sidebar.slider(
            field_name_mapping[field_name], min_val, max_val, value=current_value
        )

# Format and display user options as a table with full field names
user_options_df = pd.DataFrame(
    [{"Field": field_name_mapping[key], "Value": value} for key, value in user_options.items()]
)
st.write('User Selected Options Below')
st.table(user_options_df)

if st.button('Predict'):
    print('In button')
    data = json.dumps(user_options, indent=2)
    r = requests.post("http://127.0.0.1:8000/predict", data=data)
    response_data = r.json()
    prediction_value = response_data.get("prediction")
    if prediction_value >= 0.8:
        st.write("Prediction: Yes")
    else:
        st.write("Prediction: No")
