import redis.asyncio as redis
from src.config.constants import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

JTI_EXPIRY = 3600

token_blocklist = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    password=REDIS_PASSWORD,
    decode_responses=True
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)

async def token_in_blocklist(jti: str) -> bool:
    return await token_blocklist.exists(jti) > 0

# https://jod35.github.io/fastapi-beyond-crud-docs/site/chapter11/