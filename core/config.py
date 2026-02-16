# This is core/config.py
# Config is not business logic
#core/ = Essential, application-wide services.

# Ask this question why would this file change ?
# DB credentials change
# Deployment environment changes
# Switching from Postgres → Cloud SQL
# Switching from OpenAI → local model

# None of this is database logic , it is application configuration logic 

# Separation of Concerns: Seperating configuration from code increases maintainability and readability.

#Centralization: Instead of having configuration settings scattered across different files, all vital settings are located in one place, making them easy to find and update.
#Dependency Management: It defines the foundational rules of the application. Other parts of the application import these configurations, ensuring consistency.

import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
import redis
from langchain_redis import RedisCache
from langchain_core.globals import set_llm_cache

load_dotenv()

#postgres environment 
pg_user = os.environ["POSTGRES_USER"]
pg_password = quote_plus(os.environ["POSTGRES_PASSWORD"])
pg_host = os.environ["POSTGRES_HOST"]
pg_port = os.environ.get("POSTGRES_PORT", "5432")
pg_database = os.environ["POSTGRES_DB"]

# redis environment 
redis_cache_host=os.environ.get("REDIS_CACHE_HOST","localhost")
redis_cache_port=int(os.environ.get("REDIS_CACHE_PORT",6379))
redis_aof_host=os.environ.get("REDIS_AOF_HOST","localhost")
redis_aof_port=int(os.environ.get("REDIS_AOF_PORT",6379))

# redis connections
redis_cache_client=redis.Redis(host=redis_cache_host,port=redis_cache_port,db=0,decode_responses=True)
redis_aof_client=redis.Redis(host=redis_aof_host,port=redis_aof_port,db=0,decode_responses=True)

# Setting langchain redis cache for prompts and responses of llm in langchain
# we can also use semantic cache but for our purpose this is enough
set_llm_cache(RedisCache(redis_client=redis_cache_client))

# Postgres DATABASE URL
DATABASE_URL = (
    f"postgresql+psycopg2://{pg_user}:{pg_password}"
    f"@{pg_host}:{pg_port}/{pg_database}"
)
