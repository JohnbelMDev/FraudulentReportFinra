import pandas as pd
from sklearn.ensemble import IsolationForest
import smtplib
from email.mime.text import MIMEText

# Step 1: Load Transaction Data
# Simulated data for transaction analysis
data = {
    'TransactionID': [1, 2, 3, 4, 5],
    'Amount': [100, 250000, 150, 1000000, 200],
    'AccountAgeInYears': [2, 10, 1, 15, 3],
    'TransactionTime': [1, 23, 12, 3, 18],  # Hour of transaction
    'IsInternational': [0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

# Step 2: Feature Selection for Anomaly Detection
features = ['Amount', 'AccountAgeInYears', 'TransactionTime', 'IsInternational']
X = df[features]

# Step 3: Apply Isolation Forest for Anomaly Detection
model = IsolationForest(contamination=0.2, random_state=42)
df['IsSuspicious'] = model.fit_predict(X)

# Labeling anomalies (-1 indicates anomaly)
df['IsSuspicious'] = df['IsSuspicious'].apply(lambda x: 'Yes' if x == -1 else 'No')

# Step 4: Filter Suspicious Transactions
suspicious_transactions = df[df['IsSuspicious'] == 'Yes']

# Step 5: Reporting Mechanism
def send_report(suspicious_data):
    report = suspicious_data.to_string(index=False)
    msg = MIMEText(f"Suspicious Transactions Detected:\n\n{report}")
    msg['Subject'] = 'Fraudulent Activity Alert'
    msg['From'] = 'compliance@yourfirm.com'
    msg['To'] = 'finra-reporting@finra.org'

    try:
        with smtplib.SMTP('smtp.yourfirm.com', 587) as server:
            server.starttls()
            server.login('your_email', 'your_password')
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print("Report sent successfully.")
    except Exception as e:
        print(f"Failed to send report: {e}")

# Step 6: Generate and Send Report
if not suspicious_transactions.empty:
    send_report(suspicious_transactions)
else:
    print("No suspicious activity detected.")

# Output Results
print("Transaction Analysis Complete")
print(df)
