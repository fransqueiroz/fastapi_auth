import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://docker:docker@localhost:5432/maga_dados"
)