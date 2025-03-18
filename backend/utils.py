import random
import string   

# Generate random short code
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
