# 🤖 AI Resume Analyzer

An AI-powered Resume Analyzer that analyzes a candidate's resume against a given job description and provides useful insights such as **resume score, matching skills, missing skills, and improvement suggestions**.

The application uses **Python, Streamlit, and Google Gemini AI** to provide intelligent resume analysis.

## 🚀 Features

- 📄 Upload and analyze resumes
- 💼 Compare resume with a job description
- 🤖 AI-powered analysis using Google Gemini
- 📊 Resume-job matching score
- ✅ Identify matching skills
- ❌ Identify missing skills
- 💡 Get personalized improvement suggestions
- 🎯 Helps candidates improve their resumes for specific job roles
- 🖥️ Simple and user-friendly Streamlit interface

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Google Gemini API**
- **PyMuPDF / PDF processing**
- **python-dotenv**
- **Git & GitHub**

## 📂 Project Structure

```text
AI-Resume_Analyzer/
│
├── analyzer.py          # AI resume analysis logic
├── app.py               # Streamlit application
├── resume_parser.py     # Resume text extraction
├── requirements.txt     # Required Python packages
├── .env                 # API key configuration (not uploaded)
├── .gitignore           # Git ignored files
└── README.md            # Project documentation
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Vamshi0250/AI-Resume-Analyzer.git
```

### 2. Open the project folder

```bash
cd AI-Resume-Analyzer
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 API Key Configuration

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your Google Gemini API key.

> ⚠️ Never upload your API key or `.env` file to GitHub.

## ▶️ Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔄 How It Works

```text
Resume PDF
     ↓
Resume Text Extraction
     ↓
Job Description
     ↓
Google Gemini AI
     ↓
Resume Analysis
     ↓
Score + Matching Skills + Missing Skills
     ↓
Improvement Suggestions
```

## 📊 Example Analysis

The application can provide information such as:

- **Resume Match Score**
- **Matching Skills**
- **Missing Skills**
- **Relevant Experience**
- **Areas for Improvement**
- **Suggestions for the Candidate**

## 🎯 Use Cases

This project can be useful for:

- Students preparing for placements
- Job seekers
- Freshers
- Resume optimization
- Job-specific resume analysis
- Identifying skill gaps

## 🔮 Future Improvements

- 📌 ATS compatibility score
- 📌 Multiple resume comparison
- 📌 Job recommendation system
- 📌 Resume keyword optimization
- 📌 Resume improvement suggestions
- 📌 Support for multiple file formats
- 📌 Deployment with Streamlit Cloud

## 👨‍💻 Author

**Vamshi Goud**

B.Tech – Artificial Intelligence & Data Science

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.
