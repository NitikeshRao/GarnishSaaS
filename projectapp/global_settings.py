import random
import string
import hashlib

# Length of the random string
length = 8  # Adjust the length as needed
otp_length = 6  # Adjust the length as needed

# Generate a random string of uppercase, lowercase letters and digits
APPLICATION_ID = ''.join(random.choices(string.digits, k=length))
EMAIL_OTP = ''.join(random.choices(string.digits, k=otp_length))
MOBILE_OTP = ''.join(random.choices(string.digits, k=otp_length))

# Generate the temporary password
TEMP_PASSWORD = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Hash the temporary password using SHA-256
HASHED_TEMP_PASSWORD = hashlib.sha256(TEMP_PASSWORD.encode()).hexdigest()