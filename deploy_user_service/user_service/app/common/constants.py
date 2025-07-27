# user_service/app/common/constants.py
# Constants for User Service 
# OTP Related
OTP_LENGTH = 6
OTP_EXPIRY_SECONDS = 300  # 5 minutes
OTP_RETRY_LIMIT = 3

# JWT
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Messages
MSG_OTP_SENT = "✅ OTP sent successfully"
MSG_OTP_INVALID = "❌ Invalid OTP"
MSG_OTP_EXPIRED = "⚠️ OTP expired"
MSG_OTP_VERIFIED = "✅ OTP verified"
MSG_USER_NOT_FOUND = "❌ User not registered"
MSG_TOO_MANY_REQUESTS = "🚫 Too many requests, please try again later"
MSG_LOGIN_SUCCESS = "✅ Login successful"

# Other
DEFAULT_ENV = "dev"
