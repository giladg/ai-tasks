from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

from app.config import get_settings

settings = get_settings()


class TokenEncryption:
    """
    Utility class for encrypting and decrypting OAuth tokens using Fernet.
    OAuth tokens are encrypted before storing in the database for security.
    """

    def __init__(self):
        self.cipher = Fernet(settings.ENCRYPTION_KEY.encode())

    def encrypt(self, token: str) -> str:
        """
        Encrypt a token string.

        Args:
            token: The plain text token to encrypt

        Returns:
            Encrypted token as string
        """
        if not token:
            return ""
        return self.cipher.encrypt(token.encode()).decode()

    def decrypt(self, encrypted_token: str) -> str:
        """
        Decrypt an encrypted token.

        Args:
            encrypted_token: The encrypted token string

        Returns:
            Plain text token
        """
        if not encrypted_token:
            return ""
        return self.cipher.decrypt(encrypted_token.encode()).decode()


# Global instance for token encryption
token_encryptor = TokenEncryption()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary containing claims to encode in JWT
        expires_delta: Optional expiration time delta. If not provided, uses default from settings.

    Returns:
        JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token string

    Returns:
        Dictionary containing decoded claims, or None if token is invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def generate_fernet_key() -> str:
    """
    Generate a new Fernet encryption key.
    This is a utility function for initial setup.

    Returns:
        Base64-encoded Fernet key as string
    """
    return Fernet.generate_key().decode()


if __name__ == "__main__":
    # Utility: Generate a new Fernet key for ENCRYPTION_KEY
    print("Generated Fernet Key (use this for ENCRYPTION_KEY):")
    print(generate_fernet_key())
