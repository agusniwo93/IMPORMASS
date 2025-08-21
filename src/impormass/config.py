from pathlib import Path
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

APP_ENV = os.getenv("APP_ENV", "dev")
DB_PATH = ROOT / os.getenv("DB_PATH", "data/facturador.db")
ASSETS = ROOT / "assets"
