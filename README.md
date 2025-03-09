# Job Market Analysis & Recommendation System

This repository contains a **Job Market Analysis & Recommendation System**, built using **Streamlit** and **Plotly**. The project provides insights into job market trends and recommends jobs based on a user's skills.

## 🚀 Features

### 📊 Job Market Analysis Dashboard
- **Exploratory Data Analysis (EDA):**
  - Visualize in-demand skills, salary distributions, top industries, and job trends over time.
  - Interactive charts and graphs powered by **Plotly**.
  - Filtering options for locations, industries, experience levels, and salary range.
  
### 🔍 Job Recommendation System
- **Personalized job recommendations** based on user-inputted skills.
- Uses **TF-IDF Vectorization** and **Cosine Similarity** to find the best job matches.
- Weighted scoring system incorporating skill match and salary.
- Provides insights on missing skills to help users upskill.

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/job-market-analysis.git
   cd job-market-analysis
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## 📂 Project Structure
```
job-market-analysis/
│── app.py               # Main Streamlit app
│── eda.py               # EDA dashboard functions
│── recommendation.py     # Job recommendation logic
│── db.py                # Database connection and data fetching
│── README.md            # Documentation (this file)
│── logo.jpg             # Logo for UI branding
```

## 🏗️ How It Works
1. **Data Fetching**: The app loads job market data using `db.py`.
2. **EDA**: The `eda.py` script generates insights using **Pandas** and **Plotly**.
3. **Job Matching**: The `recommendation.py` script processes user-inputted skills using **TF-IDF** and **Cosine Similarity**.
4. **Interactive UI**: The app provides **real-time filtering** and **dynamic visualizations** using **Streamlit**.

## 📌 Example Screenshots

![image](https://github.com/user-attachments/assets/d9090890-1e40-4935-a7ee-1e4487b773d8)

![image](https://github.com/user-attachments/assets/d01f55c5-ed55-4517-991c-7024031178c1)

![image](https://github.com/user-attachments/assets/b3618cd6-4c86-46d8-84ed-40379f266dbc)




## ✨ Acknowledgments
- **Streamlit** for making data apps easy.
- **Plotly** for interactive visualizations.
- **Scikit-learn** for machine learning utilities.

---
💡 Feel free to contribute or open an issue if you have suggestions! 🚀

