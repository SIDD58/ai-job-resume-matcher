from core.config import redis_aof_client
redis_aof_client.set(name='test',value=3)
print("Hello")
my_value=redis_aof_client.get(name='test')
# it returns byte object henxe we are converting it to string utf-8 
print(my_value.decode('utf-8'))


