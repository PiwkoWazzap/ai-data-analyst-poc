# 🤖 AI Data Analyst — Proof of Concept (PoC)

A simple **AI-powered data quality assistant** that allows business users to ask natural-language questions about their data.
The app converts questions into SQL queries, runs them against a dataset (via DuckDB), and returns both results and a natural-language summary.

# 🚀 Features

- **AI-driven data analysis** — Ask questions like
  *“Which columns have missing values?”* or
  *“What are the average and max transaction values?”*
- **Generates SQL automatically** using OpenAI’s GPT models
- **Runs queries locally** on your dataset (no external database needed)
- **Streamlit chat-style UI** for interactive exploration
- **Expandable conversation history** — see previous queries and answers
- **DuckDB in-memory backend** for fast, lightweight SQL execution

## 🧠 Demo Questions

Use these to show concept viability:

1. Which columns have the most missing values?
2. What are the average, min, and max values for each numeric column?
3. Are there any outliers in the “Transaction Value” column?
4. How many unique categories are in the “Currency” column?
5. Show me rows where “Transaction Value” is greater than 10,000.

## ⚙️ Setup Instructions

### 1️⃣ Create and activate virtual environment

**Option A — Basic venv (recommended for repo portability)**

```bash
python -m venv venv
source venv/bin/activate       # on macOS/Linux
venv\Scripts\activate          # on Windows
```

### 2️⃣ Install dependencies

**Option B — Conda (if you prefer)**

<pre class="overflow-visible!" data-start="2278" data-end="2372"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>conda create -n ai-data-analyst-poc python=3.11
conda activate ai-data-analyst-poc</span></span></code></div></div></pre>

2️⃣ Install dependencies<pre class="overflow-visible!" data-start="2403" data-end="2446"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install -r requirements.txt
</span></span></code></div></div></pre>

### 3️⃣ Configure environment variables

Copy `.env.example` → `.env` and set your OpenAI key:

<pre class="overflow-visible!" data-start="2543" data-end="2590"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>OPENAI_API_KEY=sk-your-api-key-here
</span></span></code></div></div></pre>

### 4️⃣ Prepare dataset (optional)

By default, the app loads data from:

<pre class="overflow-visible!" data-start="2403" data-end="2446"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>data/Data Dump - Accrual Accounts.xlsx
</span></span></code></div></div></pre>

If you already have that file, no action is needed ✅ Otherwise, you can place your own Excel dataset there using the same name and path.

### 5️⃣Run console version (for debugging)

<pre class="overflow-visible!" data-start="2636" data-end="2661"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python app.py</span>
</span></code></div></div></pre>

Optionally for custom dataset:

<pre class="overflow-visible!" data-start="2403" data-end="2446"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python app.py --data "data/new_dataset.xlsx"
</span></span></code></div></div></pre>

### 6 Run Streamlit UI

<pre class="overflow-visible!" data-start="2688" data-end="2719"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>streamlit run streamlit_app.py
</span></span></code></div></div></pre>

Optionally for custom dataset:

<pre class="overflow-visible!" data-start="2403" data-end="2446"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>streamlit run streamlit_app.py --data "data/new_dataset.xlsx"
</span></span></code></div></div></pre>

Then open the provided local URL (e.g., [http://localhost:8501](http://localhost:8501)) in your browser.

