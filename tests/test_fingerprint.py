# True Unit test , it is a pure function
from services.fingerprint import fingerprint

# print(fingerprint("hello"))

import sys
print("sys.path output ->")
print(sys.path)
print(__name__)
def test_fingerprint_same():
    result1= fingerprint("hello")
    result2= fingerprint("hello")
    assert result1 == result2

def test_fingerprint_different():
    result1= fingerprint("hello")
    result2= fingerprint("Thello")
    assert result1 != result2
