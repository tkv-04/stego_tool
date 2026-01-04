from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def generate_key(password: str, salt: bytes) -> bytes:
    """
    Generates a key from a password and salt.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_data(data: bytes, password: str) -> bytes:
    """
    Encrypts data with a password.
    """
    salt = os.urandom(16)
    key = generate_key(password, salt)
    f = Fernet(key)
    encrypted_data = f.encrypt(data)
    return salt + encrypted_data

def decrypt_data(encrypted_data_with_salt: bytes, password: str) -> bytes:
    """
    Decrypts data with a password.
    """
    salt = encrypted_data_with_salt[:16]
    encrypted_data = encrypted_data_with_salt[16:]
    key = generate_key(password, salt)
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data
