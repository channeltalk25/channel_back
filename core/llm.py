from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Google Gemini API 키 설정 (환경변수에 있어야 함)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

# LLM 초기화
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    convert_system_message_to_human=False,
    thinking_budget=0,
)