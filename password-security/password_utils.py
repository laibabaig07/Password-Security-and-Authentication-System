import math
import random
import re
import string

COMMON_PASSWORDS = {
    "password",
    "123456",
    "qwerty",
    "abc123",
    "password123"
}


def calculate_entropy(password):

    pool_size = 0

    if any(c.isupper() for c in password):
        pool_size += 26

    if any(c.islower() for c in password):
        pool_size += 26

    if any(c.isdigit() for c in password):
        pool_size += 10

    if any(not c.isalnum() for c in password):
        pool_size += 32

    if pool_size == 0:
        return 0

    return round(len(password) * math.log2(pool_size), 2)


def estimate_crack_time(entropy):

    guesses = 2 ** entropy

    guesses_per_second = 10_000_000_000

    seconds = guesses / guesses_per_second

    if seconds < 1:
        return "Instantly cracked"

    elif seconds < 60:
        return f"{seconds:.1f} seconds"

    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"

    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"

    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days"

    else:
        return "Years or more"


def check_strength(password):

    score = 0

    if len(password) >= 12:
        score += 2

    if re.search(r'[A-Z]', password):
        score += 1

    if re.search(r'[a-z]', password):
        score += 1

    if re.search(r'[0-9]', password):
        score += 1

    if re.search(r'[^A-Za-z0-9]', password):
        score += 2

    # Check common passwords
    if password.lower() in COMMON_PASSWORDS:
        score = 0

    # Strength result
    if score <= 2:
        return "Weak"

    elif score <= 4:
        return "Moderate"

    else:
        return "Strong"


# TEST
password = input("Enter password: ")

entropy = calculate_entropy(password)

print("Strength:", check_strength(password))
print("Entropy:", entropy)
print("Crack Time:", estimate_crack_time(entropy))
def generate_strong_password(length=16):

    chars = (
        string.ascii_letters +
        string.digits +
        "!@#$%^&*()"
    )

    password = ''.join(
        random.choice(chars)
        for _ in range(length)
    )

    return password