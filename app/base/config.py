import dotenv
import os


dotenv.load_dotenv("./secrets/.env", override=True)

# 환경변수
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
