import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    POSTGRES_USER_TEST: str = os.getenv("POSTGRES_USER_TEST")
    POSTGRES_PASSWORD_TEST = os.getenv("POSTGRES_PASSWORD_TEST")
    POSTGRES_SERVER_TEST: str = os.getenv("POSTGRES_SERVER_TEST", "localhost")
    POSTGRES_PORT_TEST: str = os.getenv("POSTGRES_PORT_TEST", 65432)  # default postgres port is 5432
    POSTGRES_DB_TEST: str = os.getenv("POSTGRES_DB_TEST", "postgres")
    DATABASE_URL_TEST = f"postgresql://{POSTGRES_USER_TEST}:{POSTGRES_PASSWORD_TEST}@{POSTGRES_SERVER_TEST}:{POSTGRES_PORT_TEST}/{POSTGRES_DB_TEST}"


settings = Settings()
