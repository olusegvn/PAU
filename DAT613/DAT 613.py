# QUESTION 1.
# Function to validate password:
def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password too short"
    if len(password) > 16:
        return False, "Password too long"
    if not any(ch.isupper() for ch in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(ch.islower() for ch in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(ch.isdigit() for ch in password):
        return False, "Password must contain at least one digit."
    if not any(ch in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for ch in password):
        return False, "Password must contain at least one special character."
    return True, "===> Welcome @intuipy!."


# Test cases
class Colors:
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

passwords: list[str] = [
    'yinka',
    'shrt1A!',
    'ThisIsAVeryLongPassword123!',
    'nouppercase1!',
    'NOLOWERCASE1!',
    'NoDigits!',
    'NoSpecialChar1',
    'HelloWorld1!',
]

for pwd in passwords:
    is_valid, message = validate_password(pwd)
    color_code: str = Colors.GREEN if is_valid else Colors.FAIL
    print(f"{color_code}Password: {pwd} - Valid: {is_valid}, Message: {message}{Colors.ENDC}")



# QUESTION 2.
# Function to check if a string is a palindrome:
def is_palindrome(text: str) -> bool: return text == text[::-1] if text else False

# Test cases
print(f"It's a palindrome!") if is_palindrome("racecar") else print('Sorry, not a palindrome') # True

