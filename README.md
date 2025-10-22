# 🤖 AI Data Analyst — Proof of Concept (PoC)

A simple **AI-powered data quality assistant** that allows business users to ask natural-language questions about their data.  
The app converts questions into SQL queries, runs them against a dataset (via DuckDB), and returns both results and a natural-language summary.

---

## 🚀 Features

- **AI-driven data analysis** — Ask questions like  
  *“Which columns have missing values?”* or  
  *“What are the average and max transaction values?”*

- **Generates SQL automatically** using OpenAI’s GPT models  
- **Runs queries locally** on your dataset (no external database needed)  
- **Streamlit chat-style UI** for interactive exploration  
- **Expandable conversation history** — see previous queries and answers  
- **DuckDB in-memory backend** for fast, lightweight SQL execution  

---

## 🧠 Demo Questions

Use these to show concept viability:

1. Which columns have the most missing values?  
2. What are the average, min, and max values for each numeric column?  
3. Are there any outliers in the “Transaction Value” column?  
4. How many unique categories are in the “Currency” column?  
5. Show me rows where “Transaction Value” is greater than 10,000.

---

## 🛠️ Project Structure

```
📂 ai-data-analyst-poc/
│
├── ai_query.py           # AI query engine (OpenAI + DuckDB logic)
├── app.py                # Console demo runner
├── ui.py                 # Streamlit web UI
├── data/
│   └── Data Dump - Accrual Accounts.xlsx   # Sample dataset
├── .env.example          # Example env file
├── requirements.txt      # Dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Create and activate virtual environment

**Option A — Basic venv (recommended for repo portability)**
```bash
python -m venv venv
source venv/bin/activate       # on macOS/Linux
venv\Scripts\activate        # on Windows
```

**Option B — Conda (if you prefer)**
```bash
conda create -n ai-data-analyst-poc python=3.11
conda activate ai-data-analyst-poc
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure environment variables
Copy `.env.example` → `.env` and set your OpenAI key:

```bash
OPENAI_API_KEY=sk-your-api-key
```

### 4️⃣ Run console version (for debugging)
```bash
python app.py
```

### 5️⃣ Run Streamlit UI
```bash
streamlit run ui.py
```

Then open the provided local URL (e.g., http://localhost:8501) in your browser.

---