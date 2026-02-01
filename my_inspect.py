import inspect 

def hello(message:str,num:int):
    print(message)


hello("luck",12)
sig=inspect.signature(hello)
print(sig)
for i in sig.parameters:
    print(i)
