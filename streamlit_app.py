import os
import pandas as pd
import streamlit as st
from ai_query import AIQueryEngine
from dotenv import load_dotenv
from openai import OpenAI


@st.cache_data
def load_dataset(path: str) -> pd.DataFrame | None:
    if not os.path.exists(path):
        st.error(f"❌ Data file not found at: {path}")
        return None
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return None


def test_openai_connection(client):
    """Check if OpenAI API key works and model is accessible."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Respond with a short greeting to confirm the API connection works."}
            ],
        )
        greeting = response.choices[0].message.content
        st.success(f"✅ OpenAI connection OK: {greeting}")
    except Exception as e:
        st.error(f"❌ OpenAI connection failed: {e}")
        st.stop()


def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        st.error("❌ Missing OPENAI_API_KEY. Please set it in your .env file.")
        st.stop()
    client = OpenAI(api_key=OPENAI_API_KEY)
    test_openai_connection(client)

    DATA_PATH = "data/Data Dump - Accrual Accounts.xlsx"
    df = load_dataset(DATA_PATH)
    if df is None:
        st.stop()

    ai_engine = AIQueryEngine(client, df)

    st.set_page_config(page_title="AI Data Analyst PoC", layout="wide")
    st.markdown(
        "<style> .block-container { max-width: 900px; margin: auto; } </style>",
        unsafe_allow_html=True
    )

    st.title("AI Data Analyst")
    st.markdown("""
    Ask questions about your data in natural language.  
    The AI will generate SQL, run it on the dataset, and summarize the results.  
    Previous questions and results will stay visible.
    """)

    st.divider()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    demo_questions = [
        "How many rows have missing values?",
        "What are the average, min, and max values for each numeric column?",
        "Are there any outliers in the 'Transaction Value' column?",
        "How many unique categories are in the 'Currency' column?",
        "Show me rows where 'Transaction Value' is greater than 10000."
    ]

    st.subheader("💡 Demo Questions")
    st.caption("Click a button to try one of the sample questions:")

    cols = st.columns(len(demo_questions))
    for i, q in enumerate(demo_questions):
        if cols[i].button(q):
            user_question = q
            with st.spinner("Processing your question..."):
                answer = ai_engine.ask(user_question)
            st.session_state.chat_history.append({
                "question": user_question,
                "answer": answer
            })

    st.divider()
    user_question = st.text_input("Type your question here:")
    if user_question:
        with st.spinner("Processing your question..."):
            answer = ai_engine.ask(user_question)
        st.session_state.chat_history.append({
            "question": user_question,
            "answer": answer
        })

    st.divider()

    st.subheader("🗂️ Conversation History")
    for entry in reversed(st.session_state.chat_history):
        st.markdown(f"**Question:** {entry['question']}")

        if "error" in entry["answer"] and entry["answer"]["error"]:
            st.error(f"❌ Error: {entry['answer']['error']}")
            st.code(entry["answer"]["sql"] if "sql" in entry["answer"] else "No SQL generated")
        else:
            st.markdown("**💬 AI Summary:**")
            st.write(entry["answer"]["summary"])

            st.markdown("**🧠 Generated SQL:**")
            st.code(entry["answer"]["sql"])

            st.markdown("📊 **Result:**")
            st.dataframe(entry["answer"]["result"])

        st.divider()


if __name__ == "__main__":
    main()
