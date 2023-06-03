from cryptography.fernet import Fernet
import base64

# Custom secret key
custom_key = b"Aegis"

# Encode the custom key using URL-safe base64 encoding
converted_key = base64.urlsafe_b64encode(custom_key.ljust(32, b'\0'))

cipher_suite = Fernet(converted_key)

class Security:
    @staticmethod
    def encrypt(dongleID: str) -> str:
        encrypted_text = cipher_suite.encrypt(dongleID.encode()).decode()
        return encrypted_text

    @staticmethod
    def decrypt(encrypted_dongleID: str) -> str:
        decrypted_text = cipher_suite.decrypt(encrypted_dongleID.encode()).decode()
        return decrypted_text