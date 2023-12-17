from flask import Flask, request, jsonify
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load('rf_model.pkl')

# Preprocess and scale the input data
def preprocess_input(input_data):
    # Convert 'Gender' and 'ContractType' to numerical values
    input_data['Gender'] = 1 if input_data['Gender'] == 'Male' else 0
    contract_mapping = {'Month-to-Month': 0, 'One-Year': 1, 'Two-Year': 2}
    input_data['ContractType'] = contract_mapping[input_data['ContractType']]
    
    # Create a DataFrame from the preprocessed input data
    df = pd.DataFrame([input_data])
    
    # Scale numerical columns using the same scaler used during training
    num_cols = ['Age', 'ServiceLength', 'MonthlyCharges', 'TotalCharges']
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])
    
    return df.values[0]  # Return as a NumPy array
@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
             # Get input data from the request
        input_data = request.get_json()
        
        # Preprocess and scale the input data
        input_data = preprocess_input(input_data)
        
        # Make predictions using the model
        prediction = model.predict([input_data])[0]
        
        # Return the prediction as a JSON response
        response = {'prediction': int(prediction)}
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)})
    else:
        return "Welcome to the Churn Prediction API!"

if __name__ == '__main__':
    app.run(debug=True)
