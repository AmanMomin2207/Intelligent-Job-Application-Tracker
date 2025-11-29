<h1> Intelligent Job Application Tracker & Analyzer  </h1>

## 📌 Overview

**Intelligent Job Application Tracker & Analyzer** is an AI-powered tool designed to help job seekers:

✔ Track job applications  
✔ Analyze job descriptions  
✔ Match resumes with job requirements  
✔ Identify missing skills  
✔ Recommend better job opportunities  

Using **Natural Language Processing (NLP)**, the system compares your resume with job descriptions to provide insights such as **match score**, **missing skills**, and **keyword importance**.

---

## ✨ Features

### 🔍 Resume & Job Description Analysis
- Extracts skills, entities, and key terms using NLP models.
- Uses pretrained `.joblib` models.

### 📊 Skill Gap Detection
- Detects missing skills based on job requirements.

### 🧮 Match Score Calculation
- Converts resume & JD into vector representations.
- Uses cosine similarity to compute match percentage.

### 📁 Application Tracking
- Track all job applications (company, role, status, link, etc.).

### 🧪 Model Experiments
- Jupyter Notebook (`full_model.ipynb`) for training and evaluating models.

---

## 🧠 How It Works

### **1. Resume & JD Parsing**
- Extracts key sections and skills using NLP (`resume_entities.joblib`).

### **2. Preprocessing**
- Text cleaning  
- Tokenization  
- Vectorization (TF-IDF, Bag-of-Words)

### **3. Feature Matching**
Converts resume and job description into numerical vectors.

### **4. Similarity Score**
Uses **cosine similarity** to compute match score.

### **5. Output**
- Match percentage  
- Missing skills  
- Keyword importance  
- Recommendations  

---

## 🧰 Tech Stack

### 🔙 Backend / Core
- Python 3+
- spaCy  
- NLTK  
- scikit-learn  
- joblib

### 🛠 Development Tools
- Jupyter Notebook  
- VS Code  
- Pandas  
- NumPy  

### 📦 Dependencies  
All dependencies are listed in:
    requirements.txt


---

## 📂 Project Structure
.
├── app.py # Main script for processing resume & JDs </br>
├── parser.py # Parsing logic </br>
├── joblib_loader.py # Loads trained NLP/ML models </br>
├── full_model.ipynb # Notebook for experiments and model building </br>
├── requirements.txt # Dependencies </br>
├── resume_entities.joblib # Trained model used for entity extraction </br>
└── sample-data/ # (Optional) Resume & JD examples </br>


---

## 🚀 Getting Started

### 1️⃣ Clone the Project

git clone https://github.com/AmanMomin2207/Intelligent-Job-Application-Tracker.git </br>
cd Intelligent-Job-Application-Tracker

2️⃣ Create Virtual Environment (Optional) </br>
python -m venv venv </br>
source venv/bin/activate </br>    
Windows: venv\Scripts\activate </br>

3️⃣ Install Dependencies
pip install -r requirements.txt </br>

4️⃣ Run the Project
python app.py </br>

OR open the Jupyter Notebook: </br>

jupyter notebook

<h2> Usage </h2>
Running Resume + Job Description Matching </br>

Add your resume text file and job description text file. </br>

Update file paths in app.py: </br>
resume_path = "resume.txt" </br>
jd_path = "job.txt" </br>


Run the script:
python app.py

Output Includes:
Match Score (%)
Missing Skills
Extracted Keywords
Recommended Improvements

<h2> Future Enhancements </h2>

💡 Full web-based dashboard (Next.js) </br>
💡 Database support (PostgreSQL / MongoDB) </br>
💡 Export results as PDF </br>
💡 Auto-scan job portals </br>
💡 Transformer-based NLP (BERT/RoBERTa) </br>
💡 OCR-based PDF extraction </br>

<h2> Known Limitations </h2>

⚠ Works best for English resumes & job descriptions </br> 
⚠ Accuracy depends on input formatting </br>
⚠ No UI — currently CLI/Notebook-based </br>
⚠ NLP model may require fine-tuning for better accuracy </br>

<h2> Contributing </h2>

Contributions are welcome! </br>
Feel free to submit issues, feature requests, or pull requests. </br>
