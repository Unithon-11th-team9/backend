import dotenv
import os


dotenv.load_dotenv("./secrets/.env", override=True)

# 환경변수

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
DB_URL = os.getenv("DB_URL", "")
