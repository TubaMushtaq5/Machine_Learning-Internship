import requests

input_data = {
    "Gender": "Female",
    "Age": 30,
    "ServiceLength": 24,
    "ContractType": "One-Year",
    "MonthlyCharges": 80,
    "TotalCharges": 1500
}
response = requests.post("http://127.0.0.1:5000/", json=input_data)  # Note: URL should match your app's URL
result = response.json()

if 'prediction' in result:
    print("Churn Prediction:", result['prediction'])
else:
    print("Error:", result.get('error', 'Unknown error'))