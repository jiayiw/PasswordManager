import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

SALT_SIZE = 32
KEY_SIZE = 32
NONCE_SIZE = 12
ITERATIONS = 100000


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend(),
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt(plaintext: str, password: str) -> bytes:
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    nonce = os.urandom(NONCE_SIZE)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    return salt + nonce + ciphertext


def decrypt(encrypted_data: bytes, password: str) -> str:
    salt = encrypted_data[:SALT_SIZE]
    nonce = encrypted_data[SALT_SIZE : SALT_SIZE + NONCE_SIZE]
    ciphertext = encrypted_data[SALT_SIZE + NONCE_SIZE :]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")


def verify_password(encrypted_data: bytes, password: str) -> bool:
    try:
        decrypt(encrypted_data, password)
        return True
    except Exception:
        return False
