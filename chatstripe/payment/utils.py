from cryptography.fernet import Fernet
from django.conf import settings

key = settings.CRYPTOGRAPHY_KEY

def encrypt(data: str):
    crypter = Fernet(key)
    return crypter.encrypt(data.encode()).decode()

def decrypt(encrypted_data: str):
    crypter = Fernet(key)
    return crypter.decrypt(encrypted_data.encode()).decode()
