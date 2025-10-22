import duckdb
import pandas as pd
import re
from openai import OpenAI


class AIQueryEngine:
    def __init__(self, client: OpenAI, dataframe: pd.DataFrame):
        self.client = client
        self.df = dataframe

    def _generate_sql(self, user_question: str) -> str:
        """Ask GPT to generate a valid SQL query using DuckDB."""
        columns = list(self.df.columns)
        column_list_str = ", ".join([f'"{col}"' for col in columns])

        prompt = f"""
        You are a data analyst assistant working with a pandas DataFrame named df.
        The DataFrame has the following columns: {column_list_str}

        Generate a valid SQL query that can be executed using DuckDB (SQLite syntax).
        Only use the columns that exist.
        Return only the SQL query, do not include explanations or markdown.

        User: {user_question}
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        raw_output = response.choices[0].message.content.strip()
        sql_match = re.search(r"SELECT.*", raw_output, re.IGNORECASE | re.DOTALL)
        sql_query = sql_match.group(0).strip().strip("`") if sql_match else raw_output
        return sql_query

    def ask(self, question: str):
        """
        Process a user question:
        - Generate SQL via GPT
        - Execute SQL on DuckDB
        - Summarize the result via GPT
        """
        # Generate SQL using GPT
        sql_query = self._generate_sql(question)

        try:
            # DuckDB execution using context manager
            with duckdb.connect(database=':memory:') as con:
                # Register the pandas DataFrame as a table named 'df'
                con.register('df', self.df)

                # Execute the SQL query and fetch results as a pandas DataFrame
                result_df = con.execute(sql_query).fetchdf()

            # Summarize the result using GPT
            summary = self._summarize_result(question, result_df)

            # Return the full response
            return {
                "sql": sql_query,
                "result": result_df,
                "summary": summary
            }

        except Exception as e:
            # Handle any errors gracefully
            return {
                "error": str(e),
                "sql": sql_query,
                "result": None,
                "summary": None
            }

    def _summarize_result(self, question: str, result_df: pd.DataFrame) -> str:
        """Ask GPT to summarize the SQL result in plain English."""
        result_preview = result_df.head(5).to_markdown(index=False)

        prompt = f"""
        You are a helpful data analyst.
        The user asked: "{question}"

        Here is the result (first few rows):
        {result_preview}

        Please summarize the finding in 1-2 short sentences in plain English.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )

        return response.choices[0].message.content.strip()
