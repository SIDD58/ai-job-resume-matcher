import hashlib
def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# it is on its own a service , pure function and it can be tested independetly 
