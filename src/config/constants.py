import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://docker:docker@localhost:5432/maga_dados"
)
JWT_SECRET = os.getenv(
    "JWT_SECRET", "e698218fbf1d9d46b06a6c1aa41b3124"
)
JWT_ALGORITHM = "HS256"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = "Redis2019!"