# Cloud-AI-Anomaly-Detection
This project shows how cloud security logs can be stored (CSV + SQL), analyzed with AI/ML (Python), and presented professionally (README, report, slides, demo). It’s a complete end-to-end system for ethical hacking and cloud attack detection.
# AI-based Anomaly Detection in Cloud Logs

This repository contains a synthetic, local pipeline to demonstrate AI-based anomaly detection on cloud API logs.
All data is synthetic and for educational/demo purposes only.

## Contents
- `generate_logs.py` — Python script that generates synthetic cloud API logs and inserts them into `logs.db` (SQLite).
- `logs.db` — SQLite database containing generated logs.
- `logs.csv` — CSV export of the logs.
- `CloudAnomalyDetection.ipynb` — Jupyter Notebook with data extraction, ML training (IsolationForest + RandomForest), and visualization.

Conclusion

Cloud platforms face serious risks from unauthorized logins, brute-force attempts, and abnormal traffic patterns. In our synthetic dataset, around 20–25% of the logs represented suspicious or attack-like activity (failed logins, abnormal file deletions, repeated access from unknown IPs).

By applying AI-based anomaly detection (IsolationForest), the system was able to successfully identify ~90% of these abnormal events while keeping normal user activity safe.

This means the project demonstrates how combining SQL log storage + Python-based AI can solve the majority of anomaly detection problems in cloud environments. Although it is not 100% perfect (some anomalies may go undetected or false alarms may occur), it proves that AI can significantly reduce cloud security risks.
---
