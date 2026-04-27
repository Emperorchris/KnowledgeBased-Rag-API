from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LARGE_LANGUAGE_MODEL = os.getenv("LARGE_LANGUAGE_MODEL", "gpt-5.4-nano")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

INPUT_COST_PER_MILLION = float(os.getenv("INPUT_COST_PER_MILLION", 2.50))
OUTPUT_COST_PER_MILLION = float(os.getenv("OUTPUT_COST_PER_MILLION", 10.00))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOADED_FILES_DIR = os.getenv("UPLOADED_FILES_DIR", os.path.join(BASE_DIR, "uploaded_doc_files"))
CHROMA_PERSISTENCE_DIR = os.getenv("CHROMA_PERSISTENCE_DIR", os.path.join(BASE_DIR, "chroma_db"))

API_RATE_LIMIT_PER_MINUTE = int(os.getenv("API_RATE_LIMIT_PER_MINUTE", "60"))

COMPANY_NAME = os.getenv("COMPANY_NAME", "Sonichoice Logistics Serivices")
COMPANY_EMAIL = os.getenv("SUPPORT_EMAIL", "info@sonichoicelogistics.com")
COMPANY_WEBSITE = os.getenv("COMPANY_WEBSITE", "https://www.inventory.sonichoicelogistics.com")

AI_NAME = os.getenv("AI_NAME", "SonicAI")
AI_DESCRIPTION = os.getenv("AI_DESCRIPTION", f"{AI_NAME} is a powerful knowledge-based assistant designed to help you quickly find answers and insights from {COMPANY_NAME}.")
# if not all([MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, OPENAI_API_KEY]):
#     raise Exception("Missing environment variables")

required_vars = ["MYSQL_HOST", "MYSQL_PORT", "MYSQL_USER", "MYSQL_DATABASE", "OPENAI_API_KEY"]
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    raise Exception(f"Missing environment variables: {', '.join(missing)}")

