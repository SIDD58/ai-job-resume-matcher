from core.config import redis_aof_client
from datetime import date

def get_trace_name(user_id:str="global")->str:
    today = date.today()
    # observer here it might be possible that runs fail and still increment counter 
    # gap does not matter as we still get the seqeunce 
    redis_key = f"seq:{today}:{user_id}"  
    # Atomic increment
    count = redis_aof_client.incr(redis_key)
    
    # After a day is passed that key will not be use again for naming and hence needs to be removed from redis
    # We set 48h for buffer just to handle the edge case 
    # Set expiry for 48h on the first increment 
    if count == 1:
        redis_aof_client.expire(redis_key, 172800)   
    return f"llm_{count}_{today}_{user_id}"
