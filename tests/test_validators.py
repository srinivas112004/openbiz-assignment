from pydantic import BaseModel, ValidationError, constr

class S(BaseModel):
    pan: constr(regex=r'^[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}$')
    aadhaar: constr(regex=r'^[0-9]{12}$')

def test_valid():
    s = S(pan='ABCDE1234F', aadhaar='123456789012')
    assert s.pan == 'ABCDE1234F'
