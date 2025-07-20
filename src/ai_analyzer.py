import openai
import os
from src.logger import setup_logger, log_info, log_error
from dotenv import load_dotenv

load_dotenv()
setup_logger("ai_analyzer_log.txt")

IO_SECRET_KEY = os.getenv("IO_SECRET_KEY")

class AIAnalyzer:
    def summarize(self, article: str) -> str:
        prompt = """You are an AI agent analyzing crypto news and tweet according to news.

        1. Read the content.
        2. Decide if the news is important enough to share on Twitter (based on potential market impact).
        3. If it's important, write a short, engaging tweet (max 280 characters) that captures the essence of the news.
        4. If the article is not important enough, just write "No tweet needed."

        - As response write the tweet or "No tweet needed"
        """
        client = openai.OpenAI(
            api_key=IO_SECRET_KEY,
            base_url="https://api.intelligence.io.solutions/api/v1/",
        )

        response = client.chat.completions.create(
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": article},
            ],
            temperature=0.7,
            stream=False,
            max_completion_tokens=50
        )

        result = response.choices[0].message.content
        if result:
            log_info("Analyzed successfully.")
            return result
        else:
            log_error("Error occurred")
            return None
