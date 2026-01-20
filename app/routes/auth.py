from fastapi import APIRouter , Depends , HTTPException , status
from app.schemas.user import LoginSchema , TokenResponse, OTPRequest , OTPVerify
from app.core.database import get_db
from app.core.security import create_access_token , verify_password
from app.utils.otp import generate_otp , verify_otp

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login" , response_model=TokenResponse)
async def login(data : LoginSchema , db = Depends(get_db)):
    user = await db.users.find_one(
        {"email" : data.email , "deleted_at" : None}
    )
    
    if not user: 
        raise HTTPException(status_code=401 , detail="Invalid Credentials")
    
    if not verify_password(data.password , user["password"]):
        raise HTTPException(status_code=401 , detail="Invalid Credentials")
    
    token = create_access_token({"sub" : str(user["_id"])})
    
    return {"access_token" :  token}


@router.post("/send-otp")
async def send_otp(data : OTPRequest):
    
    otp = generate_otp(data.phone)
    print(f"OTP for {data.phone}: {otp}")
    
    return {"message" : "OTP sent Successfully"}


@router.post("/verify-otp" , response_model=TokenResponse)
async def otp_verification(data : OTPVerify , db = Depends(get_db)):
    if not verify_otp(data.phone , data.otp):
        raise HTTPException(status_code=400 , detail="Invalid OTP")
    
    user = await db.users.find_one(
        {"phone" : data.phone }
    )
    
    if not user :
        raise HTTPException(status_code=404 , detail="User not found")
    
    token = create_access_token({"sub" : str(user["_id"])})
    
    return {"access_token" : token}