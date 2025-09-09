import secrets
import string

def generate_secret_key():
    """Generate a secure random secret key"""
    # Generate a URL-safe secret key
    return secrets.token_urlsafe(32)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print(f"Here is your generated SECRET_KEY:")
    print(f"SECRET_KEY={secret_key}")