from cryptography.fernet import Fernet
# 대칭키 암호화(Symmetric Encryption) 중 하나인 Fernet(AES 기반 암호화) 를 사용


def decrypt_secret_key(encrypted_key, DECRYPTION_KEY) -> str:
    cipher_suite = Fernet(DECRYPTION_KEY.encode())  # 복호화 키로 Fernet 객체 생성
    decrypted_key = cipher_suite.decrypt(
        encrypted_key.encode()).decode()  # 복호화 후 문자열 변환
    return decrypted_key
