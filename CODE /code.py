import sqlite3
import pandas as pd
from pathlib import Path
DB = 'logs.db'
if not Path(DB).exists():
    raise FileNotFoundError('logs.db not found - put logs.db in the same folder as this notebook (or run generate_logs.py)')
conn = sqlite3.connect(DB)
df = pd.read_sql_query('SELECT * FROM logs LIMIT 10', conn)
df.head()


query = '''
SELECT user, substr(timestamp,1,16) AS minute,
  COUNT(*) AS request_count,
  AVG(response_time) AS avg_response_time,
  SUM(bytes) AS total_bytes,
  COUNT(DISTINCT api) AS unique_apis,
  SUM(CASE WHEN status != 200 THEN 1 ELSE 0 END) AS errors,
  MAX(is_anomaly) AS label
FROM logs
GROUP BY user, minute
'''

df_feat = pd.read_sql_query(query, conn, parse_dates=['minute'])
df_feat.head()


# Training IsolationForest (unsupervised) and RandomForest (supervised)
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X = df_feat[['request_count','avg_response_time','total_bytes','unique_apis','errors']].fillna(0)
y = df_feat['label'].fillna(0).astype(int)
scaler = StandardScaler()
Xs = scaler.fit_transform(X)

iso = IsolationForest(n_estimators=200, contamination=max(0.01, y.mean()), random_state=42)
iso.fit(Xs)
iso_preds = (iso.predict(Xs) == -1).astype(int)
print('IsolationForest classification report (using synthetic labels to evaluate):')
print(classification_report(y, iso_preds))

X_train, X_test, y_train, y_test = train_test_split(Xs, y, test_size=0.3, random_state=42, stratify=y)
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)
print('RandomForest classification report:')
print(classification_report(y_test, rf_preds))


# Save flagged top anomalies to CSV
import pandas as pd
df_feat['iso_score'] = iso.decision_function(Xs)
df_feat['iso_pred'] = iso_preds
df_feat.sort_values('iso_score', inplace=True)
df_feat.to_csv('results_flagged.csv', index=False)
print('Saved results_flagged.csv')

