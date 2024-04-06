import dotenv
import os


dotenv.load_dotenv("./secrets/.env", override=True)

# 환경변수
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
