# 📘 Mini Data Pipeline Project  
### *Web Scraping → SQL Storage → Data Cleaning → Anomaly Detection → Reporting*

The goal is to to simulate a small real-world data workflow using a simple website (`books.toscrape.com`), storing the results in a database, cleaning the dataset, analyzing it, and detecting anomalies.

---

## 🚀 Project Overview

This project implements an end-to-end data pipeline:

1. **Web Scraping** – extract structured book data from `https://books.toscrape.com`
2. **Database Storage** – save the data into a local SQLite database
3. **Data Cleaning & Preprocessing** – handle missing values, duplicates, data types
4. **Exploratory Data Analysis (EDA)** – basic statistics and visualizations
5. **Anomaly Detection** – identify unusual prices or ratings
6. **Reporting & Visualization** – charts and summary plots

---

## 🧰 Technology Stack

### Core Languages
- **Python 3** – scraping, pipeline logic, data processing
- **SQL** (PostgreSQL) – structured storage and querying

### Python Libraries

**Data handling**
- `pandas`
- `numpy`

**Web scraping**
- `requests`
- `beautifulsoup4`

**Anomaly detection / ML**
- `scikit-learn`
- `pyod`

**Visualization**
- `matplotlib`
- `seaborn`

**Environment / tooling**
- PostgreSQL (local file, `data/books.db`)
- Jupyter Notebook / JupyterLab
- Git + GitHub

---

