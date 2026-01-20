import random
from datetime import datetime , UTC , timedelta

OTP_STORE = {}

def generate_otp(phone : str):
    otp = str(random.randint(100000 , 999999))
    OTP_STORE[phone] = {
        "otp" : otp ,
        "expires_at" : datetime.now(UTC) + timedelta(minutes=5)
    }
    
    return otp


def verify_otp(phone : str , otp : str) -> bool :
    data =  OTP_STORE.get(phone)
    if not data:
        return False
    
    if data["expires_at"] < datetime.now(UTC):
        OTP_STORE.pop(phone , None)
        return False
    
    if data["otp"] != otp:
        return False
    
    OTP_STORE.pop(phone , None)
    return True