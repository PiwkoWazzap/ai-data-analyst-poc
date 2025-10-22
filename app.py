import os
import pandas as pd
from ai_query import AIQueryEngine
from dotenv import load_dotenv
from openai import OpenAI


def load_dataset(path: str) -> pd.DataFrame | None:
    if not os.path.exists(path):
        print(f"❌ Data file not found at: {path}")
        return None
    try:
        df = pd.read_excel(path)
        print(f"✅ Data loaded: {len(df)} rows × {len(df.columns)} columns")
        return df
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return None


def test_openai_connection():
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Respond with a short greeting to confirm the API connection works."}],
        )
        print("✅ OpenAI connection OK:", response.choices[0].message.content)
    except Exception as e:
        print("❌ OpenAI connection failed:", e)


def main():
    print("🚀 Starting AI Data Analyst PoC...")

    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("❌ Missing OPENAI_API_KEY. Please set it in your .env file.")
    client = OpenAI(api_key=OPENAI_API_KEY)
    test_openai_connection()

    DATA_PATH = "data/Data Dump - Accrual Accounts.xlsx"
    df = load_dataset(DATA_PATH)
    if df is None:
        print("⚠️ No dataset loaded. Exiting.")
        exit(1)

    ai_engine = AIQueryEngine(client, df)

    demo_questions = [
        "How many rows have missing values?",
        "What are the average, min, and max values for each numeric column?",
        "Are there any outliers in the 'Transaction Value' column?",
        "How many unique categories are in the 'Currency' column?",
        "Show me rows where 'Transaction Value' is greater than 10000."
    ]

    # Run each question
    for question in demo_questions:
        print("\n" + "="*60)
        print(f"🤖 Question: {question}\n")
        answer = ai_engine.ask(question)

        if "error" in answer and answer["error"]:
            print(f"❌ Error: {answer['error']}")
            print(f"SQL generated:\n{answer['sql']}")
        else:
            print(f"\n💬 Summary:\n{answer['summary']}")
            print(f"🧠 Generated SQL:\n{answer['sql']}")
            print(f"\n📊 Result:\n{answer['result']}")


if __name__ == "__main__":
    main()
